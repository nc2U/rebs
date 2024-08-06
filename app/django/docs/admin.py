from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Group, Category, LawsuitCase, Document, Link, File, Image


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Group)
class GroupAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'issue_project', 'name', 'order', 'search_able')
    list_display_links = ('name',)
    list_editable = ('project', 'issue_project', 'order', 'search_able')
    search_fields = ('name',)
    list_filter = ('company', 'project', 'issue_project')
    inlines = (CategoryInline,)


@admin.register(Category)
class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'group', 'color', 'name', 'parent', 'order')
    list_display_links = ('name',)
    list_editable = ('group', 'color', 'parent', 'order')
    search_fields = ('name',)
    list_filter = ('group',)


@admin.register(LawsuitCase)
class LawsuitCaseAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'sort', 'level', '__str__', 'plaintiff', 'defendant', 'case_start_date')
    list_display_links = ('__str__',)
    list_editable = ('project', 'sort', 'level', 'case_start_date',)
    list_filter = ('project', 'sort', 'level')
    search_fields = ('case_number', 'case_name', 'plaintiff', 'defendant')


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1


class FileInline(admin.TabularInline):
    model = File
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Document)
class DocumentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'group', 'is_notice', 'project', 'category', 'title', 'execution_date')
    list_display_links = ('title',)
    list_editable = ('group', 'is_notice', 'project', 'category', 'execution_date')
    search_fields = ('title', 'content')
    list_filter = ('group', 'is_notice', 'project', 'category')
    inlines = (LinkInline, FileInline, ImageInline)