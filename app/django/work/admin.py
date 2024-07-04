from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from import_export.admin import ImportExportMixin
from .models import (IssueProject, Module, Role, Permission, Member, Tracker, IssueCategory,
                     IssueStatus, Workflow, Version, Repository, CodeActivity, CodeIssuePriority,
                     CodeDocsCategory, Issue, IssueRelation, IssueFile, IssueComment, TimeEntry,
                     News, NewsFile, ActivityLogEntry, IssueLogEntry)


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class MemberInline(admin.TabularInline):
    model = Member
    extra = 0


class VersionInline(admin.TabularInline):
    model = Version
    extra = 0


class IssueCategoryInline(admin.TabularInline):
    model = IssueCategory
    extra = 0


class RepositoryInline(admin.TabularInline):
    model = Repository
    extra = 0


@admin.register(IssueProject)
class IssueProjectAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('pk', 'name', 'real_project', 'homepage', 'is_public', 'parent', 'slug', 'status', 'created')
    list_display_links = ('name',)
    inlines = (ModuleInline, MemberInline, VersionInline, IssueCategoryInline, RepositoryInline)


class PermissionInline(admin.StackedInline):
    model = Permission
    extra = 1


@admin.register(Role)
class RoleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'issue_visible', 'time_entry_visible', 'user_visible', 'default_time_activity')
    inlines = (PermissionInline,)


@admin.register(Member)
class MemberAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('user', 'project', 'get_roles', 'created')
    list_editable = ('project',)

    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()]) if obj.roles.all() else '-'

    get_roles.short_description = '역할'


@admin.register(Version)
class VersionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('project', 'name', 'status', 'get_sharing_display', 'effective_date', 'wiki_page_title')
    list_display_links = ('name',)


@admin.register(Tracker)
class TrackerAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('pk', 'name', 'is_in_roadmap', 'default_status', 'description', 'order')
    list_display_links = ('name',)
    list_editable = ('is_in_roadmap', 'default_status', 'description', 'order')
    list_filter = ('default_status',)


@admin.register(IssueCategory)
class IssueCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('project', 'name', 'assigned_to')
    list_display_links = ('name',)
    list_editable = ('project', 'assigned_to')


@admin.register(IssueStatus)
class IssueStatusAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'closed', 'order', 'user')


@admin.register(Workflow)
class WorkflowAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('role', 'tracker', 'old_status', 'get_new_statuses')

    def get_new_statuses(self, obj):
        return ", ".join([status.name for status in obj.new_statuses.all()]) if obj.new_statuses.all() else '-'

    get_new_statuses.short_description = '허용 업무 상태'


@admin.register(Repository)
class RepositoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('project', 'get_scm_display', 'is_default', 'slug', 'path', 'path_encoding', 'is_report')


@admin.register(CodeActivity)
class CodeActivityAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'active', 'default', 'user')
    list_editable = ('active', 'default')


@admin.register(CodeIssuePriority)
class CodeIssuePriorityAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'active', 'default', 'user')
    list_editable = ('active', 'default')


@admin.register(CodeDocsCategory)
class CodeDocsCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'active', 'default', 'user')
    list_editable = ('active', 'default')


class IssueFileInline(admin.TabularInline):
    model = IssueFile
    extra = 1


class IssueCommentInline(admin.TabularInline):
    model = IssueComment
    extra = 1


class TimeEntryInline(admin.TabularInline):
    model = TimeEntry
    extra = 1


class IssueRelationInline(admin.TabularInline):
    model = IssueRelation
    fk_name = 'issue'
    extra = 1


@admin.register(Issue)
class IssueAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('project', 'tracker', 'is_private', 'subject',
                    'parent', 'status', 'priority', 'start_date', 'due_date')
    list_display_links = ('subject',)
    list_filter = ('project', 'tracker', 'status', 'priority',
                   ('start_date', DateRangeFilter), ('due_date', DateRangeFilter))
    search_fields = ('subject',)
    inlines = (IssueFileInline, IssueCommentInline, TimeEntryInline, IssueRelationInline)


class NewsFileInline(admin.TabularInline):
    model = NewsFile
    extra = 1


@admin.register(News)
class NewsAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('project', 'title', 'summary', 'author')
    list_display_links = ('title',)
    inlines = (NewsFileInline,)


@admin.register(ActivityLogEntry)
class ActivityLogEntryAdmin(admin.ModelAdmin):
    list_display = ('sort', 'project', 'issue', 'spent_time', 'act_date')


@admin.register(IssueLogEntry)
class IssueLogEntryAdmin(admin.ModelAdmin):
    list_display = ('issue', 'action', 'comment_id', 'details', 'diff', 'timestamp')
