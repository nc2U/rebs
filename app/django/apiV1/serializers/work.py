from rest_framework import serializers

from work.models import (TaskProject, Module, Version, TaskCategory, Repository, Member, Role,
                         Permission, Tracker, Status, Workflow, CodeActivity, CodeIssuePriority,
                         CodeDocsCategory, Issue, IssueFile, IssueComment, SpentTime)


# Work --------------------------------------------------------------------------
class TaskProjectSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField('username', read_only=True)

    class Meta:
        model = TaskProject
        fields = ('pk', 'name', 'desc', 'identifier', 'homepage', 'is_public',
                  'is_inherit_members', 'created', 'company', 'parent_project', 'user')


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
