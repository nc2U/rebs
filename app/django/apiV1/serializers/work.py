from django.db import transaction
from rest_framework import serializers

from work.models import (TaskProject, Module, Version, TaskCategory, Repository, Member, Role,
                         Permission, Tracker, Status, Workflow, CodeActivity, CodeIssuePriority,
                         CodeDocsCategory, Issue, IssueFile, IssueComment, SpentTime)


# Work --------------------------------------------------------------------------
class ModuleInTaskProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = (
            'pk', 'project', 'issue', 'time', 'news', 'document',
            'file', 'wiki', 'repository', 'forum', 'calendar', 'gantt')


class TaskProjectSerializer(serializers.ModelSerializer):
    sub_projects = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField('username', read_only=True)
    module = ModuleInTaskProjectSerializer(read_only=True)

    class Meta:
        model = TaskProject
        fields = ('pk', 'name', 'desc', 'identifier', 'homepage', 'is_public', 'is_inherit_members',
                  'created', 'company', 'parent_project', 'depth', 'sub_projects', 'user', 'module')

    def get_sub_projects(self, obj):
        return self.__class__(obj.taskproject_set.all(), many=True, read_only=True).data

    @transaction.atomic
    def create(self, validated_data):
        parent = validated_data.get('parent_project', None)
        validated_data['depth'] = 1 if parent is None else parent.depth + 1
        project = TaskProject.objects.create(**validated_data)
        project.save()

        issue = self.initial_data.get('issue', True)
        time = self.initial_data.get('time', True)
        news = self.initial_data.get('news', True)
        document = self.initial_data.get('document', True)
        file = self.initial_data.get('file', True)
        wiki = self.initial_data.get('wiki', True)
        repository = self.initial_data.get('repository', False)
        forum = self.initial_data.get('forum', True)
        calendar = self.initial_data.get('calendar', True)
        gantt = self.initial_data.get('gantt', True)

        Module(project=project,
               issue=issue,
               time=time,
               news=news,
               document=document,
               file=file,
               wiki=wiki,
               repository=repository,
               forum=forum,
               calendar=calendar,
               gantt=gantt).save()

        return project

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        parent = validated_data.get('parent_project', None)
        instance.depth = 1 if parent is None else parent.depth + 1
        instance.save()

        issue = self.initial_data.get('issue', True)
        time = self.initial_data.get('time', True)
        news = self.initial_data.get('news', True)
        document = self.initial_data.get('document', True)
        file = self.initial_data.get('file', True)
        wiki = self.initial_data.get('wiki', True)
        repository = self.initial_data.get('repository', False)
        forum = self.initial_data.get('forum', True)
        calendar = self.initial_data.get('calendar', True)
        gantt = self.initial_data.get('gantt', True)

        module = instance.module
        module.issue = issue
        module.time = time
        module.news = news
        module.document = document
        module.file = file
        module.wiki = wiki
        module.repository = repository
        module.forum = forum
        module.calendar = calendar
        module.gantt = gantt
        module.save()

        return instance


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'


class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = '__all__'


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'


class CodeActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeActivity
        fields = '__all__'


class CodeIssuePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeIssuePriority
        fields = '__all__'


class CodeDocsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeDocsCategory
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class IssueFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueFile
        fields = '__all__'


class IssueCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueComment
        fields = '__all__'


class SpentTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpentTime
        fields = '__all__'
