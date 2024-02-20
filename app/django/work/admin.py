from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import (TaskProject, Role, Permission, Tracker, Module, Version,
                     TaskCategory, Repository, Status, Workflow, TimeActivity,
                     CodeTimeClassify, CodePriority, CodeDocsCate, Task, TaskFile, TaskComment)


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


@admin.register(TimeActivity)
class TimeActivityAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(CodeTimeClassify)
class CodeTimeClassifyAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(CodePriority)
class CodePriorityAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(CodeDocsCate)
class CodeDocsCateAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 1


class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = (TaskFileInline, TaskCommentInline)
