from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Group, Board, Category, LawsuitCase, Post, Image, File, Link, Comment, Tag


@admin.register(Group)
class GroupAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Board)
class BoardAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'group', 'name', 'order', 'search_able')
    list_display_links = ('name',)
    list_editable = ('group', 'order', 'search_able')
    search_fields = ('name',)
    list_filter = ('group',)
    inlines = (CategoryInline,)


@admin.register(Category)
class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'board', 'name', 'parent', 'order')
    list_display_links = ('name',)
    list_editable = ('board', 'parent', 'order')
    search_fields = ('name',)
    list_filter = ('board',)


@admin.register(LawsuitCase)
class LawsuitCaseAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('project', 'sort', 'level', '__str__', 'plaintiff', 'defendant', 'case_start_date')
    list_display_links = ('__str__',)
    list_editable = ('project', 'sort', 'level', 'case_start_date',)
    list_filter = ('project', 'sort', 'level')
    search_fields = ('case_number', 'plaintiff', 'defendant')


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1


class FileInline(admin.TabularInline):
    model = File
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'board', 'is_notice', 'project', 'category', 'title', 'execution_date')
    list_display_links = ('title',)
    list_editable = ('board', 'is_notice', 'project', 'category', 'execution_date')
    search_fields = ('title', 'content')
    list_filter = ('board', 'is_notice', 'project', 'category')
    inlines = (LinkInline, FileInline, CommentInline)


@admin.register(Tag)
class TagAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'board', 'name')
    list_editable = ('name',)
    search_fields = ('name',)
    list_filter = ('board',)
