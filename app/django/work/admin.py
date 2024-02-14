from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import TaskProject, Role, Permission, Tracker, Status, TaskCategory, \
    TimeActivity, Priority, DocsCategory, Task, TaskFile, TaskComment


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


@admin.register(Status)
class TaskStatusAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(TaskCategory)
class TaskCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(TimeActivity)
class TimeActivityAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(Priority)
class TimeActivityPriorityAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(DocsCategory)
class DocsCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
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
