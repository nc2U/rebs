from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import (TaskProject, Role, Permission, Tracker, Module, Version,
                     TaskCategory, Repository, Status, Workflow, CodeActivity,
                     CodeIssuePriority, CodeDocsCategory, Issue, IssueFile, IssueComment, SpentTime)


@admin.register(TaskProject)
class TaskProjectAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class PermissionInline(admin.StackedInline):
    model = Permission
    extra = 1


@admin.register(Role)
class RoleAdmin(ImportExportMixin, admin.ModelAdmin):
    inlines = (PermissionInline,)


@admin.register(Tracker)
class TaskTrackerAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(Module)
class ModuleAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(Version)
class VersionAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(TaskCategory)
class TaskCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(Repository)
class RepositoryAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(Status)
class TaskStatusAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(Workflow)
class WorkflowAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(CodeActivity)
class CodeActivityAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(CodeIssuePriority)
class CodeIssuePriorityAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(CodeDocsCategory)
class CodeDocsCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class IssueFileInline(admin.TabularInline):
    model = IssueFile
    extra = 1


class IssueCommentInline(admin.TabularInline):
    model = IssueComment
    extra = 1


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    inlines = (IssueFileInline, IssueCommentInline)


@admin.register(SpentTime)
class SpentTimeAdmin(ImportExportMixin, admin.ModelAdmin):
    pass