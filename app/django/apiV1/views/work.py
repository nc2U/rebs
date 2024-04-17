from django.db.models import Q
from rest_framework import viewsets
from django_filters.rest_framework import (FilterSet, BooleanFilter,
                                           DateFilter, CharFilter)

from ..permission import *
from ..pagination import *
from ..serializers.work import *

from django.db import models
from work.models import (IssueProject, Role, Permission, Member, Module, Version,
                         IssueCategory, Repository, Tracker, IssueStatus, Workflow,
                         CodeActivity, CodeIssuePriority, CodeDocsCategory, Issue,
                         IssueFile, IssueComment, TimeEntry, Search, ActivityLogEntry, IssueLogEntry)


# Work --------------------------------------------------------------------------
class IssueProjectFilter(FilterSet):
    parent__isnull = BooleanFilter(field_name='parent', lookup_expr='isnull', label='최상위 프로젝트')
    status__exclude = CharFilter(field_name='status', exclude=True, label='사용여부-제외')
    project = CharFilter(field_name='slug', lookup_expr='exact', label='프로젝트')
    project__exclude = CharFilter(field_name='slug', exclude=True, label='프로젝트-제외')
    is_public__exclude = BooleanFilter(field_name='is_public', exclude=True, label='공개여부-제외')
    name = CharFilter(field_name='name', lookup_expr='icontains', label='이름')
    description = CharFilter(field_name='description', lookup_expr='icontains', label='설명')

    class Meta:
        model = IssueProject
        fields = ('parent__slug', 'status', 'project', 'is_public', 'name', 'description')


class IssueProjectViewSet(viewsets.ModelViewSet):
    queryset = IssueProject.objects.all()
    serializer_class = IssueProjectSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    filterset_class = IssueProjectFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    search_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (permissions.IsAuthenticated,)


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = (permissions.IsAuthenticated,)


class TrackerViewSet(viewsets.ModelViewSet):
    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    search_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IssueStatusViewSet(viewsets.ModelViewSet):
    queryset = IssueStatus.objects.all()
    serializer_class = IssueStatusSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    search_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CodeActivityViewSet(viewsets.ModelViewSet):
    queryset = CodeActivity.objects.all()
    serializer_class = CodeActivitySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    search_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CodeIssuePriorityViewSet(viewsets.ModelViewSet):
    queryset = CodeIssuePriority.objects.all()
    serializer_class = CodeIssuePrioritySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    search_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CodeDocsCategoryViewSet(viewsets.ModelViewSet):
    queryset = CodeDocsCategory.objects.all()
    serializer_class = CodeDocsCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    search_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IssueCategoryViewSet(viewsets.ModelViewSet):
    queryset = IssueCategory.objects.all()
    serializer_class = IssueCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)


class IssueFilter(FilterSet):
    status__exclude = CharFilter(field_name='status', exclude=True, label='사용여부-제외')
    project__exclude = CharFilter(field_name='project__slug', exclude=True, label='프로젝트-제외')
    project__search = CharFilter(field_name='project__slug', label='프로젝트-검색')
    tracker__exclude = CharFilter(field_name='tracker', exclude=True, label='유형-제외')

    class Meta:
        model = Issue
        fields = ('project__slug', 'status__closed', 'status', 'tracker')

    def filter_queryset(self, queryset):
        """
        Filter the queryset with the underlying form's `cleaned_data`. You must
        call `is_valid()` or `errors` before calling this method.

        This method should be overridden if additional filtering needs to be
        applied to the queryset before it is cached.
        """
        subs = None

        def get_sub_projects(parent):
            sub_projects = []
            children = IssueProject.objects.filter(parent=parent)
            for child in children:
                sub_projects.append(child)
                sub_projects.extend(get_sub_projects(child))
            return sub_projects

        for name, value in self.form.cleaned_data.items():
            if name == 'project__slug':
                try:
                    project = IssueProject.objects.get(slug=value)
                    subs = get_sub_projects(project)
                except IssueProject.DoesNotExist:
                    pass
            if subs is not None:
                for sub in subs:
                    queryset |= sub.issue_set.filter(closed__isnull=True)

            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(
                queryset, models.QuerySet
            ), "Expected '%s.%s' to return a QuerySet, but got a %s instead." % (
                type(self).__name__,
                name,
                type(queryset).__name__,
            )
        return queryset


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    filterset_class = IssueFilter

    def get_queryset(self):
        user = self.request.user
        return self.queryset if user.is_superuser else self.queryset.filter(project__is_public=True)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updater=self.request.user)


class IssueFileViewSet(viewsets.ModelViewSet):
    queryset = IssueFile.objects.all()
    serializer_class = IssueFileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    search_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IssueCommentViewSet(viewsets.ModelViewSet):
    queryset = IssueComment.objects.all()
    serializer_class = IssueCommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    search_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TimeEntryFilter(FilterSet):
    project__search = CharFilter(field_name='project__slug', label='프로젝트-검색')
    project__exclude = CharFilter(field_name='project__slug', exclude=True, label='프로젝트-제외')
    from_spent_on = DateFilter(field_name='spent_on', lookup_expr='gte', label='작업일자부터')
    to_spent_on = DateFilter(field_name='spent_on', lookup_expr='lte', label='작업일자부터')
    user__exclude = CharFilter(field_name='user', exclude=True, label='사용자-제외')

    class Meta:
        model = TimeEntry
        fields = ('project__slug', 'spent_on', 'issue', 'user', 'activity', 'hours',
                  'issue__tracker', 'issue__parent', 'issue__fixed_version', 'issue__category')

    def filter_queryset(self, queryset):
        subs = None

        def get_sub_projects(parent):
            sub_projects = []
            children = IssueProject.objects.filter(parent=parent)
            for child in children:
                sub_projects.append(child)
                sub_projects.extend(get_sub_projects(child))
            return sub_projects

        for name, value in self.form.cleaned_data.items():
            if name == 'project__slug':
                try:
                    project = IssueProject.objects.get(slug=value)
                    subs = get_sub_projects(project)
                except IssueProject.DoesNotExist:
                    pass
            if subs is not None:
                for sub in subs:
                    queryset |= sub.timeentry_set.all()

            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(
                queryset, models.QuerySet
            ), "Expected '%s.%s' to return a QuerySet, but got a %s instead." % (
                type(self).__name__,
                name,
                type(queryset).__name__,
            )
        return queryset


class TimeEntryViewSet(viewsets.ModelViewSet):
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationTwenty
    filterset_class = TimeEntryFilter
    search_fields = ('issue__subject', 'comment')

    def get_queryset(self):
        user = self.request.user
        return self.queryset if user.is_superuser else self.queryset.filter(issue__project__is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def sort_filter(queryset, name, value):
    if value:
        queryset = queryset.filter(sort__in=value.split(","))
    return queryset


class ActivityLogFilter(FilterSet):
    project__search = CharFilter(field_name='project__slug', label='프로젝트-검색')
    from_act_date = DateFilter(field_name='act_date', lookup_expr='gte', label='로그일자부터')
    to_act_date = DateFilter(field_name='act_date', lookup_expr='lte', label='로그일자까지')
    sort = CharFilter(method=sort_filter)

    class Meta:
        model = ActivityLogEntry
        fields = ('project__slug', 'from_act_date', 'to_act_date', 'user', 'sort')

    def filter_queryset(self, queryset):
        subs = None

        def get_sub_projects(parent):
            sub_projects = []
            children = IssueProject.objects.filter(parent=parent)
            for child in children:
                sub_projects.append(child)
                sub_projects.extend(get_sub_projects(child))
            return sub_projects

        for name, value in self.form.cleaned_data.items():
            if name == 'project__slug':
                try:
                    project = IssueProject.objects.get(slug=value)
                    subs = get_sub_projects(project)
                except IssueProject.DoesNotExist:
                    pass
            if subs is not None:
                for sub in subs:
                    queryset |= sub.activitylogentry_set.all()

            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(
                queryset, models.QuerySet
            ), "Expected '%s.%s' to return a QuerySet, but got a %s instead." % (
                type(self).__name__,
                name,
                type(queryset).__name__,
            )
        return queryset


class ActivityLogEntryViewSet(viewsets.ModelViewSet):
    queryset = ActivityLogEntry.objects.all()
    serializer_class = ActivityLogEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationThreeHundred
    filterset_class = ActivityLogFilter

    def get_queryset(self):
        user = self.request.user
        return self.queryset if user.is_superuser else self.queryset.filter(project__is_public=True)


class IssueLogEntryViewSet(viewsets.ModelViewSet):
    queryset = IssueLogEntry.objects.all()
    serializer_class = IssueLogEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginationThreeHundred
    filterset_fields = ('issue', 'user')

    def get_queryset(self):
        user = self.request.user
        return self.queryset if user.is_superuser else self.queryset.filter(issue__project__is_public=True)


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    permission_classes = (permissions.IsAuthenticated,)
