from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Forum, PostCategory, Post, PostFile, PostImage, Comment, Tag


class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


@admin.register(Forum)
class ForumAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'name', 'description', 'search_able')
    list_display_links = ('project', 'name',)
    list_select_related = ('project',)
    list_editable = ('description', 'search_able')
    search_fields = ('name',)
    list_filter = ('project',)
    inlines = (CategoryInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project')


@admin.register(PostCategory)
class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'forum', 'color', 'name', 'parent', 'order')
    list_display_links = ('name',)
    list_select_related = ('forum', 'parent')
    list_editable = ('forum', 'color', 'parent', 'order')
    search_fields = ('name',)
    list_filter = ('forum',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('forum', 'parent')


class FileInline(admin.TabularInline):
    model = PostFile
    extra = 1


class ImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'forum', 'category', 'title', 'is_notice', 'creator', 'created')
    list_display_links = ('title',)
    list_select_related = ('forum', 'category', 'creator')
    list_editable = ('forum', 'category', 'is_notice')
    search_fields = ('title', 'content')
    list_filter = ('forum', 'is_notice', 'category')
    date_hierarchy = 'created'
    inlines = (FileInline, ImageInline, CommentInline)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('forum', 'category', 'creator')


@admin.register(Comment)
class CommentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'post', 'creator', 'content', 'like', 'created')
    list_display_links = ('id', 'content')
    list_select_related = ('post', 'creator')
    search_fields = ('content', 'creator__username')
    list_filter = ('created', 'secret')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post', 'creator')


@admin.register(Tag)
class TagAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'forum', 'name')
    list_display_links = ('id',)
    list_select_related = ('forum',)
    list_editable = ('name',)
    search_fields = ('name',)
    list_filter = ('forum',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('forum')
