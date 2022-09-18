from rest_framework import serializers

from accounts.models import User
from document.models import (Group, Board, Category, LawsuitCase,
                             Post, Image, Link, File, Comment, Tag)


# Document --------------------------------------------------------------------------
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name', 'manager')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('pk', 'group', 'name', 'order', 'search_able', 'manager')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'board', 'name', 'parent', 'order')


class LawSuitCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawsuitCase
        fields = ('pk', 'project', 'sort', 'level', 'related_case', 'court',
                  'other_agency', 'case_number', 'case_name', 'plaintiff',
                  'defendant', 'related_debtor', 'case_start_date', 'summary')


class PostSerializer(serializers.ModelSerializer):
    proj_name = serializers.SlugField(source='project', read_only=True)
    cate_name = serializers.SlugField(source='category', read_only=True)
    comments = serializers.RelatedField(many=True, read_only=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = ('pk', 'board', 'is_notice', 'project', 'proj_name', 'category', 'cate_name',
                  'lawsuit', 'title', 'execution_date', 'content', 'is_hide_comment', 'hit',
                  'like', 'dislike', 'blame', 'ip', 'device', 'secret', 'password', 'links',
                  'files', 'comments', 'user', 'soft_delete', 'created', 'updated')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('pk', 'post', 'image')


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('pk', 'post', 'link', 'hit')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('pk', 'post', 'file', 'hit')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'pk', 'post', 'content', 'like', 'dislike', 'blame', 'ip',
            'device', 'secret', 'password', 'soft_delete')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('pk', 'board', 'tag', 'post')
