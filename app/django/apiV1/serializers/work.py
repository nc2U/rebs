from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers

from accounts.models import User
from work.models import (IssueProject, Role, Permission, Member, Module, Version,
                         IssueCategory, Repository, Tracker, IssueStatus, Workflow,
                         CodeActivity, CodeIssuePriority, CodeDocsCategory, Issue,
                         IssueFile, IssueComment, TimeEntry, Search, ActivityLogEntry, IssueLogEntry)


# Work --------------------------------------------------------------------------
class FamilyTreeSerializer(serializers.ModelSerializer):
    """ recursive get patents -> for bread crumb """

    class Meta:
        model = IssueProject
        fields = ('pk', 'name', 'slug')


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
        fields = ('pk', 'user', 'roles')


class ModuleInIssueProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('pk', 'project', 'issue', 'time', 'news', 'document',
                  'file', 'wiki', 'repository', 'forum', 'calendar', 'gantt')


class TrackerInIssueProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = ('pk', 'name')


class IssueProjectSerializer(serializers.ModelSerializer):
    family_tree = FamilyTreeSerializer(many=True, read_only=True)
    sub_projects = serializers.SerializerMethodField()
    all_members = MemberInIssueProjectSerializer(many=True, read_only=True)
    members = MemberInIssueProjectSerializer(many=True, read_only=True)
    trackers = TrackerInIssueProjectSerializer(many=True, read_only=True)
    module = ModuleInIssueProjectSerializer(read_only=True)
    visible = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField('username', read_only=True)

    class Meta:
        model = IssueProject
        fields = ('pk', 'company', 'name', 'slug', 'description', 'homepage', 'is_public',
                  'family_tree', 'parent', 'is_inherit_members', 'default_version',
                  'trackers', 'status', 'depth', 'all_members', 'members', 'sub_projects',
                  'module', 'visible', 'user', 'created', 'updated')

    def get_sub_projects(self, obj):
        return self.__class__(obj.issueproject_set.exclude(status='9'), many=True, read_only=True).data

    def get_visible(self, obj):
        request = self.context.get('request')

        def final_members(proj):
            # 상속받는 상위 멤버 모두 구하기
            total_members = proj.members.all()

            if proj.is_inherit_members and proj.parent:
                parent_members = final_members(proj.parent)
                total_members |= parent_members

            return total_members

        if request and hasattr(request, 'user'):
            user = request.user
            members = [m.user.pk for m in final_members(obj)]
            return obj.is_public or user.pk in members or user.is_superuser
        else:
            return False

    @transaction.atomic
    def create(self, validated_data):
        parent = validated_data.get('parent', None)
        validated_data['depth'] = 1 if parent is None else parent.depth + 1
        project = IssueProject.objects.create(**validated_data)
        # 프로젝트 생성시 설정된 기본 유형 추가
        project.trackers.add(*[1, 2, 3])
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
        parent = validated_data.get('parent', None)
        instance.depth = 1 if parent is None else parent.depth + 1

        subs = instance.issueproject_set.all()
        is_public = validated_data.get('is_public', None)
        if is_public and is_public is not instance.is_public:
            for sub in subs:
                sub.is_public = is_public
                sub.save()

        status = validated_data.get('status', None)
        if status == '9':
            for sub in subs:
                sub.status = status
                sub.save()

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
                user_instance = User.objects.get(pk=user)
                member_instance = Member.objects.create(user=user_instance)
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


class MemberSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    roles = RoleInMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = ('pk', 'user', 'roles')


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('pk', 'project', 'issue', 'time', 'news', 'document',
                  'file', 'wiki', 'repository', 'forum', 'calendar', 'gantt')


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('pk', 'project', 'name', 'status', 'sharing',
                  'due_date', 'description', 'wiki_page_title')


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ('pk', 'project', 'scm', 'is_default',
                  'slug', 'path', 'path_encoding', 'is_report')


class TrackerSerializer(serializers.ModelSerializer):
    projects = FamilyTreeSerializer(many=True, read_only=True)

    class Meta:
        model = Tracker
        fields = ('pk', 'name', 'description', 'is_in_roadmap', 'default_status',
                  'projects', 'order', 'user', 'created', 'updated')


class IssueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueStatus
        fields = ('pk', 'name', 'description', 'closed', 'order', 'user', 'created', 'updated')


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ('pk', 'role', 'tracker', 'old_status', 'new_statuses')


class CodeActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeActivity
        fields = ('pk', 'name', 'active', 'default', 'order', 'user', 'created', 'updated')


class CodeIssuePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeIssuePriority
        fields = ('pk', 'name', 'active', 'default', 'order', 'user', 'created', 'updated')


class CodeDocsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeDocsCategory
        fields = ('pk', 'name', 'active', 'default', 'order', 'user', 'created', 'updated')


class IssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueCategory
        fields = ('pk', 'project', 'name', 'assigned_to')


class IProjectIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueProject
        fields = ('slug', 'name')


class IssueStatusInIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueStatus
        fields = ('pk', 'name', 'closed')


class CodePriorityInIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeIssuePriority
        fields = ('pk', 'name')


class IssueSerializer(serializers.ModelSerializer):
    project = IProjectIssueSerializer(read_only=True)
    tracker = TrackerInIssueProjectSerializer(read_only=True)
    status = IssueStatusInIssueSerializer(read_only=True)
    priority = CodePriorityInIssueSerializer(read_only=True)
    assigned_to = SimpleUserSerializer(read_only=True)
    parent = serializers.SerializerMethodField()
    spent_time = serializers.SerializerMethodField(read_only=True)
    creator = SimpleUserSerializer(read_only=True)
    updater = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ('pk', 'project', 'tracker', 'status', 'priority', 'subject',
                  'description', 'category', 'fixed_version', 'assigned_to', 'parent',
                  'watchers', 'is_private', 'estimated_hours', 'start_date', 'due_date',
                  'done_ratio', 'closed', 'spent_time', 'creator', 'updater', 'created', 'updated')

    @staticmethod
    def get_parent(obj):
        # Check if there is a parent object corresponding to the parent field in the entire collection
        parent_obj = IssueProject.objects.filter(id=obj.parent_id).first() if obj.parent else None
        return obj.parent if parent_obj else None

    @staticmethod
    def get_spent_time(obj):
        return obj.timeentry_set.all().aggregate(Sum('hours'))['hours__sum']

    @transaction.atomic
    def create(self, validated_data):
        project = IssueProject.objects.get(slug=self.initial_data.get('project', None))
        tracker = Tracker.objects.get(pk=self.initial_data.get('tracker'))
        status = IssueStatus.objects.get(pk=self.initial_data.get('status'))
        priority = CodeIssuePriority.objects.get(pk=self.initial_data.get('priority'))
        assigned_to = self.initial_data.get('assigned_to', None)
        assigned_to = User.objects.get(pk=assigned_to) if assigned_to else None
        parent = self.initial_data.get('parent', None)
        parent = Issue.objects.get(pk=parent) if parent else None

        # Pop 'watchers' from validated_data to avoid KeyError
        watchers = validated_data.pop('watchers', [])
        issue = Issue.objects.create(project=project,
                                     tracker=tracker,
                                     status=status,
                                     priority=priority,
                                     assigned_to=assigned_to,
                                     parent=parent,
                                     **validated_data)
        # Set the watchers of the instance to the list of watchers
        user = self.context['request'].user
        issue.watchers.add(user.pk)
        if watchers:
            for watcher in watchers:
                if not issue.watchers.filter(id=watcher.pk).exists():
                    issue.watchers.add(watcher)
        return issue

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.project = IssueProject.objects.get(slug=self.initial_data.get('project', None))
        instance.tracker = Tracker.objects.get(pk=self.initial_data.get('tracker'))
        instance.status = IssueStatus.objects.get(pk=self.initial_data.get('status'))
        instance.closed = timezone.now() if instance.status.closed else None
        instance.priority = CodeIssuePriority.objects.get(pk=self.initial_data.get('priority'))
        assigned_to = self.initial_data.get('assigned_to', None)
        instance.assigned_to = User.objects.get(pk=assigned_to) if assigned_to else None
        parent = self.initial_data.get('parent', None)
        instance.parent = Issue.objects.get(pk=parent) if parent else None

        watchers = validated_data.get('watchers', [])
        if watchers:
            for watcher in watchers:
                if not instance.watchers.filter(id=watcher.pk).exists():
                    instance.watchers.set(watcher)
        # time entry logic
        hours = self.initial_data.get('hours', None)
        activity = self.initial_data.get('activity', None)
        comment = self.initial_data.get('comment', None)
        user = self.context['request'].user
        if hours and activity:
            activity = CodeActivity.objects.get(pk=activity)
            TimeEntry.objects.create(issue=instance, hours=hours,
                                     activity=activity, comment=comment, user=user)
        # issue_comment logic
        comment_content = self.initial_data.get('comment_content', None)
        if comment_content:
            IssueComment.objects.create(issue=instance, content=comment_content, user=user)

        return super().update(instance, validated_data)


class IssueInRelatedSerializer(serializers.ModelSerializer):
    project = IProjectIssueSerializer(read_only=True)
    tracker = serializers.SlugRelatedField(slug_field='name', read_only=True)
    status = IssueStatusInIssueSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ('pk', 'project', 'tracker', 'status', 'subject', 'description')


class IssueFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueFile
        fields = ('pk', 'issue', 'file', 'description')


class IssueCommentSerializer(serializers.ModelSerializer):
    issue = IssueInRelatedSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = IssueComment
        fields = ('pk', 'issue', 'content', 'created', 'updated', 'user')


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

        time_entry = TimeEntry.objects.create(issue_id=issue,
                                              activity_id=activity,
                                              **validated_data)
        return time_entry

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.issue = Issue.objects.get(pk=self.initial_data.get('issue'))
        instance.activity = CodeActivity.objects.get(pk=self.initial_data.get('activity'))
        return super().update(instance, validated_data)


class TimeEntryInActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = ('pk', 'hours', 'comment')


class ActivityLogEntrySerializer(serializers.ModelSerializer):
    project = IProjectIssueSerializer(read_only=True)
    issue = IssueInRelatedSerializer(read_only=True)
    comment = IssueCommentSerializer(read_only=True)
    spent_time = TimeEntryInActivityLogSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = ActivityLogEntry
        fields = ('pk', 'sort', 'project', 'issue', 'status_log', 'comment',
                  'spent_time', 'act_date', 'timestamp', 'user')
        # 'change_sets', 'news', 'document', 'file', 'wiki', 'message',


class IssueLogEntrySerializer(serializers.ModelSerializer):
    issue = IssueInRelatedSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = IssueLogEntry
        fields = ('pk', 'log_id', 'issue', 'action', 'details', 'diff', 'timestamp', 'user')


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'
