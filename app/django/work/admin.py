from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import (IssueProject, Member, Role, Permission, Tracker, Module,
                     Version, IssueCategory, Repository, IssueStatus, Workflow, CodeActivity,
                     CodeIssuePriority, CodeDocsCategory, Issue, IssueFile, IssueComment, TimeEntry)


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


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
    list_display = ('name', 'homepage', 'is_public', 'parent', 'slug', 'status', 'created')
    inlines = (ModuleInline, VersionInline,
               IssueCategoryInline, RepositoryInline)


class PermissionInline(admin.StackedInline):
    model = Permission
    extra = 1


@admin.register(Role)
class RoleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'issue_visible', 'time_entry_visible', 'user_visible', 'default_time_activity')
    inlines = (PermissionInline,)


@admin.register(Member)
class MemberAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(Tracker)
class TaskTrackerAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'is_in_roadmap', 'default_status', 'order')
    list_editable = ('is_in_roadmap', 'default_status', 'order')


@admin.register(IssueStatus)
class IssueStatusAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'closed')


@admin.register(Workflow)
class WorkflowAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(CodeActivity)
class CodeActivityAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'default', 'active')


@admin.register(CodeIssuePriority)
class CodeIssuePriorityAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'default', 'active')


@admin.register(CodeDocsCategory)
class CodeDocsCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'default', 'active')


class IssueFileInline(admin.TabularInline):
    model = IssueFile
    extra = 1


class IssueCommentInline(admin.TabularInline):
    model = IssueComment
    extra = 1


class TimeEntryInline(admin.TabularInline):
    model = TimeEntry
    extra = 1


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('project', 'tracker', 'is_private', 'subject',
                    'parent', 'status', 'priority', 'start_date', 'due_date')
    list_display_links = ('subject',)
    inlines = (IssueFileInline, IssueCommentInline, TimeEntryInline)
