from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import (AccountSort, AccountSubD1, AccountSubD2, AccountSubD3,
                     ProjectAccountSort, ProjectAccountD1, ProjectAccountD2,
                     WiseSaying)


class AccountSortAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


class AccountSubD2Inline(admin.TabularInline):
    model = AccountSubD2
    extra = 2


class AccountSubD1Admin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    inlines = (AccountSubD2Inline,)


class AccountSubD3Inline(admin.TabularInline):
    model = AccountSubD3
    extra = 2


class AccountSubD2Admin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'd1', 'name', 'code', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    list_filter = ('d1',)
    inlines = (AccountSubD3Inline,)


class AccountSubD3Admin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'd2', 'name', 'code', 'description', 'is_hide', 'is_special')
    list_display_links = ('name',)
    list_editable = ('is_hide', 'is_special')
    search_fields = ('name', 'description')
    list_filter = ('d2__d1', 'd2')


class ProjectAccountD2Inline(ImportExportMixin, admin.TabularInline):
    model = ProjectAccountD2


class ProjectAccountSortAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


class ProjectAccountD1Admin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'acc', 'code', 'name', 'description')
    list_display_links = ('code', 'name')
    list_filter = ('acc', 'sorts')
    search_fields = ('name', 'description')
    inlines = (ProjectAccountD2Inline,)


class ProjectAccountD2Admin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'd1', 'code', 'name', 'sub_title', 'description')
    list_display_links = ('code', 'name')
    list_filter = ('d1__acc', 'd1')
    search_fields = ('name', 'description')


class WiseSayingAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(AccountSort, AccountSortAdmin)
admin.site.register(AccountSubD1, AccountSubD1Admin)
admin.site.register(AccountSubD2, AccountSubD2Admin)
admin.site.register(AccountSubD3, AccountSubD3Admin)
admin.site.register(ProjectAccountSort, ProjectAccountSortAdmin)
admin.site.register(ProjectAccountD1, ProjectAccountD1Admin)
admin.site.register(ProjectAccountD2, ProjectAccountD2Admin)
admin.site.register(WiseSaying, WiseSayingAdmin)
