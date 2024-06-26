import json
import os.path

from django.db import transaction, IntegrityError
from django.db.models import Sum, Q
from django.utils import timezone
from rest_framework import serializers

from accounts.models import User
from work.models import (IssueProject, Role, Permission, Member, Module, Version,
                         IssueCategory, Repository, Tracker, IssueStatus, Workflow,
                         CodeActivity, CodeIssuePriority, CodeDocsCategory, Issue, IssueRelation,
                         IssueFile, IssueComment, TimeEntry, Search, ActivityLogEntry, IssueLogEntry, News)


# Work --------------------------------------------------------------------------
class SimpleIssueProjectSerializer(serializers.ModelSerializer):
    visible = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = IssueProject
        fields = ('pk', 'name', 'slug', 'visible')

    def get_visible(self, obj):
        request = self.context.get('request')

        if request and hasattr(request, 'user'):
            user = request.user
            visible_auth = user.work_manager or user.is_superuser
            all_members = obj.all_members()
            members = [m.user.pk for m in all_members]
            return obj.is_public or user.pk in members or visible_auth
        else:
            return False


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


class RoleInMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('pk', 'name')


class MemberInIssueProjectSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    roles = RoleInMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = ('pk', 'user', 'roles', 'created')


class ModuleInIssueProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('pk', 'project', 'issue', 'time', 'news', 'document',
                  'file', 'wiki', 'repository', 'forum', 'calendar', 'gantt')


class RoleInIssueProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('pk', 'name')


class TrackerInIssueProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = ('pk', 'name', 'description')


class VersionInIssueProjectSerializer(serializers.ModelSerializer):
    status_desc = serializers.CharField(source='get_status_display', read_only=True)
    sharing_desc = serializers.CharField(source='get_sharing_display', read_only=True)
    is_default = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Version
        fields = ('pk', 'name', 'status', 'status_desc', 'sharing', 'sharing_desc',
                  'is_default', 'effective_date', 'description', 'wiki_page_title')

    @staticmethod
    def get_is_default(obj):
        default_ver = obj.project.default_version
        return True if default_ver and default_ver.pk == obj.pk else False


class IssueCategoryInIssueProjectSerializer(serializers.ModelSerializer):
    assigned_to = SimpleUserSerializer(read_only=True)

    class Meta:
        model = IssueCategory
        fields = ('pk', 'name', 'assigned_to')


class CodeActivityInIssueProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeActivity
        fields = ('pk', 'name', 'active', 'default', 'order')


class IssueProjectSerializer(serializers.ModelSerializer):
    family_tree = SimpleIssueProjectSerializer(many=True, read_only=True)
    module = ModuleInIssueProjectSerializer(read_only=True)
    all_members = MemberInIssueProjectSerializer(many=True, read_only=True)
    members = MemberInIssueProjectSerializer(many=True, read_only=True)
    allowed_roles = RoleInIssueProjectSerializer(many=True, read_only=True)
    trackers = TrackerInIssueProjectSerializer(many=True, read_only=True)
    versions = VersionInIssueProjectSerializer(many=True, read_only=True)
    categories = IssueCategoryInIssueProjectSerializer(many=True, read_only=True)
    activities = CodeActivityInIssueProjectSerializer(many=True, read_only=True)
    visible = serializers.SerializerMethodField(read_only=True)
    total_estimated_hours = serializers.SerializerMethodField(read_only=True)
    total_time_spent = serializers.SerializerMethodField(read_only=True)
    parent_visible = serializers.SerializerMethodField(read_only=True)
    sub_projects = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField('username', read_only=True)

    class Meta:
        model = IssueProject
        fields = ('pk', 'company', 'real_project', 'name', 'slug', 'description', 'homepage',
                  'is_public', 'module', 'is_inherit_members', 'allowed_roles', 'trackers', 'versions',
                  'default_version', 'categories', 'status', 'depth', 'all_members', 'members', 'activities',
                  'visible', 'total_estimated_hours', 'total_time_spent', 'family_tree', 'parent',
                  'parent_visible', 'sub_projects', 'user', 'created', 'updated',)

    def get_sub_projects(self, obj):
        sub_projects = obj.issueproject_set.exclude(status='9')
        request = self.context.get('request')

        return self.__class__(sub_projects, many=True, read_only=True, context=self.context).data

    def get_visible(self, obj):
        request = self.context.get('request')

        if request and hasattr(request, 'user'):
            user = request.user
            visible_auth = user.work_manager or user.is_superuser
            all_members = obj.all_members()
            members = [m.user.pk for m in all_members]
            return obj.is_public or user.pk in members or visible_auth
        else:
            return False

    def get_parent_visible(self, obj):
        return self.get_visible(obj.parent) if obj.parent else False

    def get_total_estimated_hours(self, obj):
        return self.recursive_estimated_hours(obj)

    def recursive_estimated_hours(self, project):
        total_hours = project.issue_set.aggregate(total=Sum('estimated_hours'))['total'] or 0
        sub_projects = project.issueproject_set.exclude(status='9')
        for sub_project in sub_projects:
            total_hours += self.recursive_estimated_hours(sub_project)
        return total_hours

    def get_total_time_spent(self, obj):
        return self.recursive_time_spent(obj)

    def recursive_time_spent(self, project):
        total_hours = project.timeentry_set.aggregate(total=Sum('hours'))['total'] or 0
        sub_projects = project.issueproject_set.exclude(status='9')
        for sub_project in sub_projects:
            total_hours += self.recursive_time_spent(sub_project)
        return total_hours

    @transaction.atomic
    def create(self, validated_data):
        project = IssueProject.objects.create(**validated_data)
        # 프로젝트 생성시 설정된 기본 역할 및 유형 추가
        allowed_roles = self.initial_data.get('allowed_roles', [])
        if allowed_roles:
            project.allowed_roles.add(*allowed_roles)
        trackers = self.initial_data.get('trackers', [])
        if trackers:
            project.trackers.add(*trackers)
        project.save()

        Module(project=project,
               issue=self.initial_data.get('issue', True),
               time=self.initial_data.get('time', True),
               news=self.initial_data.get('news', True),
               document=self.initial_data.get('document', True),
               file=self.initial_data.get('file', True),
               wiki=self.initial_data.get('wiki', True),
               repository=self.initial_data.get('repository', False),
               forum=self.initial_data.get('forum', True),
               calendar=self.initial_data.get('calendar', True),
               gantt=self.initial_data.get('gantt', True)).save()

        return project

    @transaction.atomic
    def update(self, instance, validated_data):
        # 역할 및 유형이 있는 경우 업데이트 로직
        allowed_roles = self.initial_data.get('allowed_roles', [])
        if allowed_roles and allowed_roles != [r.pk for r in instance.allowed_roles.all()]:
            instance.allowed_roles.set(allowed_roles)

        trackers = self.initial_data.get('trackers', [])
        if trackers and trackers != [t.pk for t in instance.trackers.all()]:
            instance.trackers.set(trackers)

        module = instance.module
        module.issue = self.initial_data.get('issue', True)
        module.time = self.initial_data.get('time', True)
        module.news = self.initial_data.get('news', True)
        module.document = self.initial_data.get('document', True)
        module.file = self.initial_data.get('file', True)
        module.wiki = self.initial_data.get('wiki', True)
        module.repository = self.initial_data.get('repository', False)
        module.forum = self.initial_data.get('forum', True)
        module.calendar = self.initial_data.get('calendar', True)
        module.gantt = self.initial_data.get('gantt', True)
        module.save()

        # user에 대응하는 member 모델 생성
        users = self.initial_data.get('users')
        roles = self.initial_data.get('roles')
        del_mem = self.initial_data.get('del_mem', None)

        members = []

        if users:
            for user in users:
                # user_instance = User.objects.get(pk=user)
                member_instance = Member.objects.create(user_id=user)
                member_instance.roles.add(*roles)
                member_instance.save()
                members.append(member_instance.pk)

            for member in members:
                instance.members.add(member)
        elif del_mem is not None:
            instance.members.remove(del_mem)
            member = Member.objects.get(pk=del_mem)
            member.delete()

        return super().update(instance, validated_data)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('pk', 'project_create', 'project_update', 'project_close', 'project_delete',
                  'project_public', 'project_module', 'project_member', 'project_version',
                  'project_create_sub', 'project_pub_query', 'project_save_query',
                  'forum_read', 'forum_create', 'forum_update', 'forum_own_update',
                  'forum_delete', 'forum_own_delete', 'forum_watcher_read',
                  'forum_watcher_create', 'forum_watcher_delete', 'forum_manage',
                  'calendar_read',
                  'document_read', 'document_create', 'document_update', 'document_delete',
                  'file_read', 'file_manage',
                  'gantt_read',
                  'issue_read', 'issue_create', 'issue_update', 'issue_own_update', 'issue_copy',
                  'issue_rel_manage', 'issue_sub_manage', 'issue_public', 'issue_own_public',
                  'issue_comment_create', 'issue_comment_update', 'issue_comment_own_update',
                  'issue_private_comment_read', 'issue_private_comment_set', 'issue_delete',
                  'issue_watcher_read', 'issue_watcher_create', 'issue_watcher_delete', 'issue_import',
                  'issue_category_manage',
                  'news_read', 'news_manage', 'news_manage', 'news_comment',
                  'repo_changesets_read', 'repo_read', 'repo_commit_access', 'repo_rel_issue_manage', 'repo_manage',
                  'time_read', 'time_create', 'time_update', 'time_own_update',
                  'time_pro_act_manage', 'time_other_user_log', 'time_entries_import',
                  'wiki_read', 'wiki_history_read', 'wiki_page_export', 'wiki_page_update',
                  'wiki_page_rename', 'wiki_page_delete', 'wiki_attachment_delete', 'wiki_watcher_read',
                  'wiki_watcher_create', 'wiki_watcher_delete', 'wiki_page_project', 'wiki_manage')


class RoleSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(read_only=True)

    class Meta:
        model = Role
        fields = ('pk', 'name', 'assignable', 'issue_visible', 'time_entry_visible', 'user_visible',
                  'default_time_activity', 'permission', 'order', 'user', 'created', 'updated')


class SimpleIssuesInMemberProjectSerializer(serializers.ModelSerializer):
    sub_projects = serializers.SerializerMethodField()

    class Meta:
        model = IssueProject
        fields = ('pk', 'name', 'slug', 'sub_projects', 'depth')

    def get_sub_projects(self, obj):
        return self.__class__(obj.issueproject_set.exclude(status='9'), many=True, read_only=True).data


class MemberSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    roles = RoleInMemberSerializer(many=True, read_only=True)
    issue_projects = SimpleIssuesInMemberProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = ('pk', 'user', 'roles', 'issue_projects', 'created')


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('pk', 'project', 'issue', 'time', 'news', 'document',
                  'file', 'wiki', 'repository', 'forum', 'calendar', 'gantt')


class IssueInVersionSerializer(serializers.ModelSerializer):
    project = SimpleIssueProjectSerializer(read_only=True)
    tracker = TrackerInIssueProjectSerializer(read_only=True)
    watchers = SimpleUserSerializer(many=True, read_only=True)
    spent_times = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ('pk', 'project', 'subject', 'status', 'tracker', 'priority',
                  'fixed_version', 'category', 'assigned_to', 'watchers',
                  'estimated_hours', 'spent_times', 'done_ratio', 'closed')

    @staticmethod
    def get_spent_times(obj):
        return obj.timeentry_set.aggregate(total=Sum('hours'))['total'] or 0


class VersionSerializer(serializers.ModelSerializer):
    project = SimpleIssueProjectSerializer(read_only=True)
    status_desc = serializers.CharField(source='get_status_display', read_only=True)
    sharing_desc = serializers.CharField(source='get_sharing_display', read_only=True)
    is_default = serializers.SerializerMethodField(read_only=True)
    issues = IssueInVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Version
        fields = ('pk', 'project', 'name', 'status', 'status_desc', 'sharing', 'sharing_desc',
                  'effective_date', 'description', 'wiki_page_title', 'issues', 'is_default')

    @staticmethod
    def get_is_default(obj):
        default_ver = obj.project.default_version
        return True if default_ver and default_ver.pk == obj.pk else False

    @transaction.atomic
    def create(self, validated_data):
        project_slug = self.initial_data.get('project')
        try:
            project = IssueProject.objects.get(slug=project_slug)
        except IssueProject.DoesNotExist:
            raise serializers.ValidationError({'project': 'Project does not exist'})

        version = Version.objects.create(**validated_data, project=project)
        is_default = self.initial_data.get('is_default', False)
        if is_default:
            project.default_version = version
            project.save()
        return version

    @transaction.atomic
    def update(self, instance, validated_data):
        project_slug = self.initial_data.get('project')
        try:
            project = IssueProject.objects.get(slug=project_slug)
            is_default = self.initial_data.get('is_default', False)
            default_version = instance if is_default else None
            project.default_version = default_version
            project.save()
        except IssueProject.DoesNotExist:
            raise serializers.ValidationError({'project': 'Project does not exist'})

        instance.__dict__.update(validated_data)
        instance.project = project
        instance.save()
        return instance


class TrackerSerializer(serializers.ModelSerializer):
    projects = SimpleIssueProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Tracker
        fields = ('pk', 'name', 'description', 'is_in_roadmap', 'default_status',
                  'projects', 'order', 'user', 'created', 'updated')


class IssueCategorySerializer(serializers.ModelSerializer):
    project = SimpleIssueProjectSerializer(read_only=True)

    class Meta:
        model = IssueCategory
        fields = ('pk', 'project', 'name', 'assigned_to')

    @transaction.atomic
    def create(self, validated_data):
        project_slug = self.initial_data.get('project')
        try:
            project = IssueProject.objects.get(slug=project_slug)
        except IssueProject.DoesNotExist:
            raise serializers.ValidationError({'project': 'Project does not exist'})

        category = IssueCategory.objects.create(**validated_data, project=project)
        return category

    @transaction.atomic
    def update(self, instance, validated_data):
        project_slug = self.initial_data.get('project')
        try:
            project = IssueProject.objects.get(slug=project_slug)
        except IssueProject.DoesNotExist:
            raise serializers.ValidationError({'project': 'Project does not exist'})

        instance.__dict__.update(**validated_data)
        instance.project = project
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.save()
        return instance


class IssueCountByTrackerSerializer(serializers.ModelSerializer):
    open = serializers.SerializerMethodField()
    closed = serializers.SerializerMethodField()

    class Meta:
        model = Tracker
        fields = ['pk', 'name', 'open', 'closed']

    def get_open(self, obj):
        issues = Issue.objects.filter(tracker=obj, closed__isnull=True)
        # Access the request object from context
        request = self.context.get('request')
        issues = self.filter_project(request, issues)
        return issues.count()

    def get_closed(self, obj):
        issues = Issue.objects.filter(tracker=obj).exclude(closed__isnull=True)
        # Access the request object from context
        request = self.context.get('request')
        issues = self.filter_project(request, issues)
        return issues.count()

    def get_sub_projects(self, parent):
        sub_projects = []

        children = IssueProject.objects.filter(parent=parent)
        for child in children:
            sub_projects.append(child)
            sub_projects.extend(self.get_sub_projects(child))
        return sub_projects

    def filter_project(self, request, issues):
        project = request.query_params.get('projects', None)
        if project is not None:
            try:
                project = IssueProject.objects.get(pk=project)
                subs = self.get_sub_projects(project)
                return issues.filter(Q(project__slug=project.slug) | Q(project__slug__in=[sub.slug for sub in subs]))
            except IssueProject.DoesNotExist:
                return issues


class IssueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueStatus
        fields = ('pk', 'name', 'description', 'closed', 'order')


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ('pk', 'role', 'tracker', 'old_status', 'new_statuses')


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ('pk', 'project', 'scm', 'is_default',
                  'slug', 'path', 'path_encoding', 'is_report')


class CodeActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeActivity
        fields = ('pk', 'name', 'active', 'default', 'order')


class CodeIssuePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeIssuePriority
        fields = ('pk', 'name', 'active', 'default', 'order')


class CodeDocsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeDocsCategory
        fields = ('pk', 'name', 'active', 'default', 'order')


class IssueStatusInIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueStatus
        fields = ('pk', 'name', 'closed')


class CodePriorityInIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeIssuePriority
        fields = ('pk', 'name')


class VersionInIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('pk', 'name')


class IssueFileInIssueSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = IssueFile
        fields = ('pk', 'file', 'file_name', 'file_type', 'file_size', 'description', 'created', 'user')


class IssueInIssueSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(read_only=True, slug_field='name')
    assigned_to = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ('pk', 'subject', 'status', 'assigned_to', 'start_date', 'estimated_hours', 'done_ratio', 'closed')


class IssueRelationInIssueSerializer(serializers.ModelSerializer):
    issue_to = IssueInIssueSerializer(read_only=True)
    type_display = serializers.CharField(source='get_relation_type_display', read_only=True)

    class Meta:
        model = IssueRelation
        fields = ('pk', 'issue', 'issue_to', 'relation_type', 'type_display', 'delay')


class IssueSerializer(serializers.ModelSerializer):
    project = SimpleIssueProjectSerializer(read_only=True)
    tracker = TrackerInIssueProjectSerializer(read_only=True)
    status = IssueStatusInIssueSerializer(read_only=True)
    priority = CodePriorityInIssueSerializer(read_only=True)
    fixed_version = VersionInIssueSerializer(read_only=True)
    assigned_to = SimpleUserSerializer(read_only=True)
    watchers = SimpleUserSerializer(many=True, read_only=True)
    spent_time = serializers.SerializerMethodField(read_only=True)
    files = IssueFileInIssueSerializer(many=True, read_only=True)
    sub_issues = serializers.SerializerMethodField()
    related_issues = serializers.SerializerMethodField()
    creator = SimpleUserSerializer(read_only=True)
    updater = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ('pk', 'project', 'tracker', 'status', 'priority', 'subject',
                  'description', 'category', 'fixed_version', 'assigned_to',
                  'parent', 'watchers', 'is_private', 'estimated_hours', 'start_date',
                  'due_date', 'done_ratio', 'closed', 'spent_time', 'files', 'sub_issues',
                  'related_issues', 'creator', 'updater', 'created', 'updated')

    @staticmethod
    def get_spent_time(obj):
        return obj.timeentry_set.all().aggregate(Sum('hours'))['hours__sum']

    @staticmethod
    def get_sub_issues(obj):
        return IssueInIssueSerializer(obj.issue_set.all().order_by('id'), many=True, read_only=True).data

    @staticmethod
    def get_related_issues(obj):
        return IssueRelationInIssueSerializer(obj.relation_issues.all().order_by('id'), many=True, read_only=True).data

    @transaction.atomic
    def create(self, validated_data):
        project = IssueProject.objects.get(slug=self.initial_data.get('project', None))
        tracker = Tracker.objects.get(pk=self.initial_data.get('tracker'))
        status = IssueStatus.objects.get(pk=self.initial_data.get('status'))
        priority = CodeIssuePriority.objects.get(pk=self.initial_data.get('priority'))
        fixed_version = self.initial_data.get('fixed_version')
        fixed_version = fixed_version if fixed_version else None
        assigned_to = self.initial_data.get('assigned_to', None)
        assigned_to = User.objects.get(pk=assigned_to) if assigned_to else None

        # Pop 'watchers' from validated_data to avoid KeyError
        issue = Issue.objects.create(project=project,
                                     tracker=tracker,
                                     status=status,
                                     priority=priority,
                                     fixed_version_id=fixed_version,
                                     assigned_to=assigned_to,
                                     **validated_data)
        # Set the watchers of the instance to the list of watchers
        user = self.context['request'].user
        issue.watchers.add(user.pk)
        watchers = self.initial_data.getlist('watchers', [])
        if watchers:
            for watcher in watchers:
                issue.watchers.add(watcher)
        # File 처리
        new_files = self.initial_data.getlist('new_files', [])
        descriptions = self.initial_data.getlist('descriptions', [])
        if new_files:
            for i, file in enumerate(new_files):
                issue_file = IssueFile(issue=issue, file=file,
                                       description=descriptions[i], user=user)
                issue_file.save()
        return issue

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        if self.initial_data.get('project', None):
            instance.project = IssueProject.objects.get(slug=self.initial_data.get('project', None))
        if self.initial_data.get('tracker'):
            instance.tracker = Tracker.objects.get(pk=self.initial_data.get('tracker'))
        if self.initial_data.get('status'):
            instance.status = IssueStatus.objects.get(pk=self.initial_data.get('status'))
        if instance.closed is None and instance.status.closed:
            instance.closed = timezone.localtime()
        elif instance.closed is not None and not instance.status.closed:
            instance.closed = None
        if self.initial_data.get('priority'):
            instance.priority = CodeIssuePriority.objects.get(pk=self.initial_data.get('priority'))
        if self.initial_data.get('fixed_version'):
            instance.fixed_version = Version.objects.get(pk=self.initial_data.get('fixed_version'))
        assigned_to = self.initial_data.get('assigned_to', None)
        instance.assigned_to = User.objects.get(pk=assigned_to) if assigned_to else None

        # 공유자 업데이트
        watchers = self.initial_data.getlist('watchers', [])
        if watchers:
            for watcher in watchers:
                instance.watchers.add(watcher)

        del_watcher = self.initial_data.get('del_watcher', None)
        if del_watcher:
            instance.watchers.remove(del_watcher)

        # sub_issue 관계 지우기
        del_child = self.initial_data.get('del_child', None)
        if del_child:
            child = instance.issue_set.get(pk=del_child)
            child.parent = None
            child.save()

        # time entry logic
        hours = self.initial_data.get('hours', None)
        activity = self.initial_data.get('activity', None)
        comment = self.initial_data.get('comment', None)
        user = self.context['request'].user
        if hours and activity:
            activity = CodeActivity.objects.get(pk=activity)
            TimeEntry.objects.create(project=instance.project, issue=instance, hours=hours,
                                     activity=activity, comment=comment, user=user)
        # issue_comment logic
        comment_content = self.initial_data.get('comment_content', None)
        if comment_content:
            IssueComment.objects.create(issue=instance, content=comment_content, user=user)

        # File 처리
        new_files = self.initial_data.getlist('new_files', [])
        descriptions = self.initial_data.getlist('descriptions', [])

        if new_files:
            for i, file in enumerate(new_files):
                issue_file = IssueFile(issue=instance, file=file,
                                       description=descriptions[i], user=user)
                issue_file.save()

        old_files = self.initial_data.getlist('files', [])
        if old_files:
            for json_file in old_files:
                file = json.loads(json_file)
                file_object = IssueFile.objects.get(pk=file.get('pk'))

                if file.get('del'):
                    file_object.delete()

        edit_file = self.initial_data.get('edit_file', None)  # pk
        cng_file = self.initial_data.get('cng_file', None)  # change file
        edit_file_desc = self.initial_data.get('edit_file_desc', None)
        if edit_file:
            file = IssueFile.objects.get(pk=edit_file)
            if cng_file:
                old_file = file.file
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
                file.file = cng_file
            if edit_file_desc:
                file.description = edit_file_desc
            file.save()

        del_file = self.initial_data.get('del_file', None)
        if del_file:
            file = IssueFile.objects.get(pk=del_file)
            file.delete()

        return super().update(instance, validated_data)


class IssueCountByMemberSerializer(serializers.Serializer):
    open_charged = serializers.IntegerField(read_only=True)
    closed_charged = serializers.IntegerField(read_only=True)
    all_charged = serializers.IntegerField(read_only=True)
    open_created = serializers.IntegerField(read_only=True)
    closed_created = serializers.IntegerField(read_only=True)
    all_created = serializers.IntegerField(read_only=True)


class IssueRelationSerializer(serializers.ModelSerializer):
    issue_to = IssueInIssueSerializer(read_only=True)
    type_display = serializers.CharField(source='get_relation_type_display', read_only=True)

    class Meta:
        model = IssueRelation
        fields = ('pk', 'issue', 'issue_to', 'relation_type', 'type_display', 'delay')

    @transaction.atomic
    def create(self, validated_data):
        issue_to = self.initial_data.get('issue_to', None)
        issue_to = Issue.objects.get(pk=issue_to) if issue_to else None
        try:
            issue_relation = IssueRelation.objects.create(issue_to=issue_to, **validated_data)
            return issue_relation
        except IntegrityError:
            raise serializers.ValidationError("해당 업무는 이미 등록되어 있는 연결된 업무입니다.")


class IssueInRelatedSerializer(serializers.ModelSerializer):
    project = SimpleIssueProjectSerializer(read_only=True)
    tracker = serializers.SlugRelatedField(slug_field='name', read_only=True)
    status = IssueStatusInIssueSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ('pk', 'project', 'tracker', 'status', 'subject', 'description')


class IssueFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueFile
        fields = ('pk', 'issue', 'file', 'description', 'created')


class IssueCommentSerializer(serializers.ModelSerializer):
    issue = IssueInRelatedSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = IssueComment
        fields = ('pk', 'issue', 'content', 'is_private', 'created', 'updated', 'user')


class SimpleCodeActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeActivity
        fields = ('pk', 'name')


class TimeEntrySerializer(serializers.ModelSerializer):
    issue = IssueInRelatedSerializer(read_only=True)
    activity = SimpleCodeActivitySerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)
    total_hours = serializers.SerializerMethodField()

    class Meta:
        model = TimeEntry
        fields = ('pk', 'issue', 'spent_on', 'hours', 'activity', 'comment',
                  'created', 'updated', 'user', 'total_hours')

    def get_total_hours(self, obj):
        # Access the filtered queryset from the view context
        filtered_queryset = self.context['view'].filter_queryset(self.context['view'].get_queryset())
        total_hours = filtered_queryset.aggregate(total_hours=Sum('hours'))
        return total_hours['total_hours'] or 0

    @transaction.atomic
    def create(self, validated_data):
        issue = self.initial_data.get('issue', None)
        activity = self.initial_data.get('activity', None)

        time_entry = TimeEntry.objects.create(project=issue.project,
                                              issue_id=issue,
                                              activity_id=activity,
                                              **validated_data)
        return time_entry

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.issue = Issue.objects.get(pk=self.initial_data.get('issue'))
        instance.project = instance.issue.project
        instance.activity = CodeActivity.objects.get(pk=self.initial_data.get('activity'))
        return super().update(instance, validated_data)


class TimeEntryInActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = ('pk', 'hours', 'comment')


class NewsSerializer(serializers.ModelSerializer):
    project = SimpleIssueProjectSerializer(read_only=True)
    author = SimpleUserSerializer(read_only=True)

    class Meta:
        model = News
        fields = ('pk', 'project', 'title', 'summary', 'description', 'author', 'created')

    @transaction.atomic
    def create(self, validated_data):
        project__slug = self.initial_data.get('project__slug', None)
        project = IssueProject.objects.get(slug=project__slug)
        news = News.objects.create(**validated_data, project=project)
        return news

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        project = self.initial_data.get('project__slug', None)
        if instance.project.slug != project:
            instance.project = IssueProject.objects.get(slug=project)
        instance.save()
        return instance


class ActivityLogEntrySerializer(serializers.ModelSerializer):
    project = SimpleIssueProjectSerializer(read_only=True)
    issue = IssueInRelatedSerializer(read_only=True)
    comment = IssueCommentSerializer(read_only=True)
    spent_time = TimeEntryInActivityLogSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = ActivityLogEntry
        fields = ('pk', 'sort', 'project', 'issue', 'status_log', 'comment',
                  'spent_time', 'act_date', 'timestamp', 'user')
        # 'change_sets', 'news', 'document', 'file', 'wiki', 'message',


class SimpleCommentInIssueLogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueComment
        fields = ('pk', 'content')


class IssueLogEntrySerializer(serializers.ModelSerializer):
    issue = IssueInRelatedSerializer(read_only=True)
    comment = SimpleCommentInIssueLogEntrySerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = IssueLogEntry
        fields = ('pk', 'log_id', 'issue', 'action', 'comment', 'details', 'diff', 'timestamp', 'user')


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'
