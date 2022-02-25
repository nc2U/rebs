from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import AccountSubD1, AccountSubD2, AccountSubD3, ProjectAccountD1, ProjectAccountD2, WiseSaying


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
    list_display = ('id', 'd2', 'name', 'code', 'description', 'is_special')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    list_filter = ('d2__d1', 'd2')


class ProjectAccountD2Inline(ImportExportMixin, admin.TabularInline):
    model = ProjectAccountD2


class ProjectAccountD1Admin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'sort', 'code', 'name', 'description')
    list_display_links = ('name',)
    inlines = (ProjectAccountD2Inline,)


class ProjectAccountD2Admin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'd1', '__str__', 'code', 'sub_title', 'name', 'description')
    list_display_links = ('__str__',)


class WiseSayingAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(AccountSubD1, AccountSubD1Admin)
admin.site.register(AccountSubD2, AccountSubD2Admin)
admin.site.register(AccountSubD3, AccountSubD3Admin)

admin.site.register(ProjectAccountD1, ProjectAccountD1Admin)
admin.site.register(ProjectAccountD2, ProjectAccountD2Admin)
admin.site.register(WiseSaying, WiseSayingAdmin)
