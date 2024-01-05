import json
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from rest_framework import serializers

from accounts.models import User, Profile
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
        fields = ('pk', 'board', 'color', 'name', 'parent', 'order')


class FilesInLawSuitCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file',)


class UserInDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


class LawSuitCaseSerializer(serializers.ModelSerializer):
    proj_name = serializers.SlugField(source='project', read_only=True)
    sort_desc = serializers.CharField(source='get_sort_display', read_only=True)
    level_desc = serializers.CharField(source='get_level_display', read_only=True)
    related_case_name = serializers.SlugField(source='related_case', read_only=True)
    court_desc = serializers.CharField(source='get_court_display', read_only=True)
    user = UserInDocumentsSerializer(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)
    files = serializers.SerializerMethodField(read_only=True)
    prev_pk = serializers.SerializerMethodField(read_only=True)
    next_pk = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LawsuitCase
        fields = ('pk', 'company', 'project', 'proj_name', 'sort', 'sort_desc', 'level', 'level_desc',
                  'related_case', 'related_case_name', 'court', 'court_desc', 'other_agency', 'case_number',
                  'case_name', '__str__', 'plaintiff', 'plaintiff_attorney', 'plaintiff_case_price',
                  'defendant', 'defendant_attorney', 'defendant_case_price', 'related_debtor', 'case_start_date',
                  'case_end_date', 'summary', 'user', 'links', 'files', 'created', 'prev_pk', 'next_pk')
        read_only_fields = ('__str__',)

    @staticmethod
    def get_links(obj):
        links = []
        posts = obj.post_set.all().order_by('id')
        for post in posts:
            category = Category.objects.get(pk=post.category.id)
            category_data = {'color': category.color, 'name': category.name}
            for link in post.links.values():
                links.append({
                    'pk': link.get('id'),
                    'category': {'name': category_data.get('name'),
                                 'color': category_data.get('color')},
                    'link': link.get('link')})
        return links

    @staticmethod
    def get_files(obj):
        files = []
        posts = obj.post_set.all().order_by('id')
        for post in posts:
            category = Category.objects.get(pk=post.category.id)
            category_data = {'color': category.color, 'name': category.name}
            for file in post.files.values():
                files.append({
                    'pk': file.get('id'),
                    'category': {'name': category_data.get('name'),
                                 'color': category_data.get('color')},
                    'file': settings.MEDIA_URL + file.get('file')})
        return files

    def get_collection(self):
        queryset = LawsuitCase.objects.all()
        query = self.context['request'].query_params
        company = query.get('company')
        is_com = query.get('is_com')
        project = query.get('project')
        sort = query.get('sort')
        level = query.get('level')
        court = query.get('court')
        in_progress = query.get('in_progress')
        related = query.get('related_case')
        search = query.get('search')

        queryset = queryset.filter(company_id=company) if company else queryset
        queryset = queryset.filter(project_id=project) if project else queryset
        queryset = queryset.filter(project__isnull=True) if is_com == 'true' else queryset
        queryset = queryset.filter(project__isnull=False) if is_com == 'false' else queryset
        queryset = queryset.filter(court=court) if court else queryset
        queryset = queryset.filter(Q(pk=related) | Q(related_case_id=related)) if related else queryset
        queryset = queryset.filter(sort=sort) if sort else queryset
        queryset = queryset.filter(level=level) if level else queryset
        queryset = queryset.filter(case_end_date__isnull=True) if in_progress == 'true' else queryset
        queryset = queryset.filter(case_end_date__isnull=False) if in_progress == 'false' else queryset
        queryset = queryset.filter(
            Q(other_agency__icontains=search) |
            Q(case_number__icontains=search) |
            Q(case_name__icontains=search) |
            Q(plaintiff__icontains=search) |
            Q(defendant__icontains=search) |
            Q(case_start_date__icontains=search) |
            Q(case_end_date__icontains=search) |
            Q(summary__icontains=search)
        ) if search else queryset

        return queryset

    def get_prev_pk(self, obj):
        prev_obj = (self.get_collection()
                    .filter(case_start_date__lt=obj.case_start_date).first())
        return prev_obj.pk if prev_obj else None

    def get_next_pk(self, obj):
        next_obj = (self.get_collection().order_by('case_start_date', 'id')
                    .filter(case_start_date__gt=obj.case_start_date).first())
        return next_obj.pk if next_obj else None


class SimpleLawSuitCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawsuitCase
        fields = ('pk', '__str__')


class LinksInPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('pk', 'post', 'link', 'hit')


class FilesInPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('pk', 'post', 'file', 'hit')


class PostSerializer(serializers.ModelSerializer):
    proj_name = serializers.SlugField(source='project', read_only=True)
    board_name = serializers.SlugField(source='board', read_only=True)
    cate_name = serializers.SlugField(source='category', read_only=True)
    lawsuit_name = serializers.SlugField(source='lawsuit', read_only=True)
    links = LinksInPostSerializer(many=True, read_only=True)
    files = FilesInPostSerializer(many=True, read_only=True)
    user = UserInDocumentsSerializer(read_only=True)
    scraped = serializers.SerializerMethodField(read_only=True)
    prev_pk = serializers.SerializerMethodField(read_only=True)
    next_pk = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('pk', 'company', 'project', 'proj_name', 'board', 'board_name', 'category',
                  'cate_name', 'lawsuit', 'lawsuit_name', 'title', 'execution_date', 'content',
                  'hit', 'like', 'scraped', 'blame', 'ip', 'device', 'is_secret', 'password',
                  'is_hide_comment', 'is_notice', 'is_blind', 'deleted', 'links', 'files',
                  'comments', 'user', 'created', 'updated', 'is_new', 'prev_pk', 'next_pk')
        read_only_fields = ('ip', 'comments')

    def get_collection(self):
        queryset = Post.objects.all()
        query = self.context['request'].query_params
        company = query.get('company')
        project = query.get('project')
        is_com = query.get('is_com')
        board = query.get('board')
        is_notice = True if query.get('is_notice') == 'true' else False
        category = query.get('category')
        lawsuit = query.get('lawsuit')
        search = query.get('search')

        queryset = queryset.filter(company_id=company) if company else queryset
        queryset = queryset.filter(project_id=project) if project else queryset
        queryset = queryset.filter(project__isnull=True) if is_com == 'true' else queryset
        queryset = queryset.filter(project__isnull=False) if is_com == 'false' else queryset
        queryset = queryset.filter(board_id=board) if board else queryset
        queryset = queryset.filter(is_notice=True) if is_notice == 'true' else queryset
        queryset = queryset.filter(is_notice=False) if is_notice == 'false' else queryset
        queryset = queryset.filter(category_id=category) if category else queryset
        queryset = queryset.filter(lawsuit_id=lawsuit) if lawsuit else queryset
        queryset = queryset.filter(
            Q(lawsuit__case_number__icontains=search) |
            Q(lawsuit__case_name__icontains=search) |
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(links__link__icontains=search) |
            Q(files__file__icontains=search) |
            Q(user__username__icontains=search)
        ) if search else queryset

        return queryset

    @staticmethod
    def get_scraped(obj):
        return len(obj.scrape_set.all())

    def get_prev_pk(self, obj):
        prev_obj = self.get_collection().filter(created__lt=obj.created).first()
        return prev_obj.pk if prev_obj else None

    def get_next_pk(self, obj):
        next_obj = self.get_collection().filter(created__gt=obj.created).order_by('created').first()
        return next_obj.pk if next_obj else None

    def to_python(self, value):

        def split_url(url):
            """
            Return a list of url parts via urlparse.urlsplit(), or raise
            ValidationError for some malformed URLs.
            """
            try:
                return list(urlsplit(url))
            except ValueError:
                # urlparse.urlsplit can raise a ValueError with some
                # misformatted URLs.
                raise ValidationError(self.error_messages['invalid'], code='invalid')

        if value:
            url_fields = split_url(value)
            if not url_fields[0]:
                # If no URL scheme given, assume http://
                url_fields[0] = 'http'
            if not url_fields[1]:
                # Assume that if no domain is provided, that the path segment
                # contains the domain.
                url_fields[1] = url_fields[2]
                url_fields[2] = ''
                # Rebuild the url_fields list, since the domain segment may now
                # contain the path too.
                url_fields = split_url(urlunsplit(url_fields))
            value = urlunsplit(url_fields)
        return value

    @transaction.atomic
    def create(self, validated_data):
        validated_data['ip'] = self.context.get('request').META.get('REMOTE_ADDR')
        post = Post.objects.create(**validated_data)

        # Links 처리
        new_links = self.initial_data.getlist('newLinks')
        if new_links:
            for link in new_links:
                Link.objects.create(post=post, link=self.to_python(link))

        # Files 처리
        new_files = self.initial_data.getlist('newFiles')
        if new_files:
            for file in new_files:
                File.objects.create(post=post, file=file)

        return post

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['ip'] = self.context.get('request').META.get('REMOTE_ADDR')
        instance.__dict__.update(**validated_data)
        instance.project = validated_data.get('project', instance.project)
        instance.board = validated_data.get('board', instance.board)
        instance.category = validated_data.get('category', instance.category)
        instance.lawsuit = validated_data.get('lawsuit', instance.lawsuit)
        instance.save()

        try:
            # Links 처리
            old_links = self.initial_data.getlist('links')
            if old_links:
                for json_link in old_links:
                    link = json.loads(json_link)
                    link_object = Link.objects.get(pk=link.get('pk'))
                    if link.get('del'):
                        link_object.delete()
                    else:
                        link_object.link = self.to_python(link.get('link'))
                        link_object.save()

            new_links = self.initial_data.getlist('newLinks')
            if new_links:
                for link in new_links:
                    Link.objects.create(post=instance, link=self.to_python(link))

            # Files 처리
            old_files = self.initial_data.getlist('files')
            if old_files:
                cng_pks = self.initial_data.getlist('cngPks')
                cng_files = self.initial_data.getlist('cngFiles')
                cng_maps = [(pk, cng_files[i]) for i, pk in enumerate(cng_pks)]

                for json_file in old_files:
                    file = json.loads(json_file)
                    file_object = File.objects.get(pk=file.get('pk'))

                    if file.get('del'):
                        file_object.delete()

                    for cng_map in cng_maps:
                        if int(file.get('pk')) == int(cng_map[0]):
                            file_object.file = cng_map[1]
                            file_object.save()

            new_files = self.initial_data.getlist('newFiles')
            if new_files:
                for file in new_files:
                    File.objects.create(post=instance, file=file)
        except AttributeError:
            pass

        return instance


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('pk', 'like')

    @transaction.atomic
    def update(self, instance, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.get(user=user)

        if profile.like_posts.filter(pk=instance.pk).exists():
            if instance.like > 0:
                instance.like -= 1
                profile.like_posts.remove(instance)
        else:
            instance.like += 1
            profile.like_posts.add(instance)
        instance.save()
        return instance


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


class SimplePostInCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('pk', 'company', 'project', 'board')


class CommentSerializer(serializers.ModelSerializer):
    post = SimplePostInCommentSerializer(read_only=True)
    replies = serializers.SerializerMethodField(read_only=True)
    user = UserInDocumentsSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('pk', 'post', 'content', 'parent', 'replies', 'like',
                  'blame', 'ip', 'device', 'secret', 'user', 'created')
        read_only_fields = ('ip',)

    def get_replies(self, instance):
        serializer = self.__class__(instance.replies, many=True)
        serializer.bind('', self)
        return serializer.data


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'like')

    @transaction.atomic
    def update(self, instance, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.get(user=user)

        if profile.like_comments.filter(pk=instance.pk).exists():
            if instance.like > 0:
                instance.like -= 1
                profile.like_comments.remove(instance)
        else:
            instance.like += 1
            profile.like_comments.add(instance)
        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('pk', 'board', 'name', 'post')
