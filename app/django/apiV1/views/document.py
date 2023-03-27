from django.db.models import Q
from rest_framework import viewsets
from django_filters import BooleanFilter
from django_filters.rest_framework import FilterSet

from ..permission import *
from ..serializers.document import *
from ..pagination import PageNumberPaginationThreeThousand

from document.models import (Group, Board, Category, LawsuitCase, Post,
                             Like, DisLike, Image, Link, File, Comment, Tag)


# Document --------------------------------------------------------------------------

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('group', 'search_able', 'manager')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('board',)


class LawSuitCaseFilterSet(FilterSet):
    is_com = BooleanFilter(field_name='project', lookup_expr='isnull', label='본사')

    class Meta:
        model = LawsuitCase
        fields = ('company', 'is_com', 'project', 'sort', 'level', 'court')


class LawSuitCaseBase(viewsets.ModelViewSet):
    queryset = LawsuitCase.objects.all()
    serializer_class = LawSuitCaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_class = LawSuitCaseFilterSet
    search_fields = ('other_agency', 'case_number', 'case_name', 'plaintiff', 'defendant', 'case_start_date', 'summary')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LawSuitCaseViewSet(LawSuitCaseBase):
    def get_queryset(self):
        queryset = LawsuitCase.objects.all()
        related = self.request.query_params.get('related_case')
        if related:
            queryset = queryset.filter(Q(pk=related) | Q(related_case=related))
        return queryset


class AllLawSuitCaseViewSet(LawSuitCaseViewSet):
    serializer_class = SimpleLawSuitCaseSerializer
    pagination_class = PageNumberPaginationThreeThousand


class PostFilterSet(FilterSet):
    is_com = BooleanFilter(field_name='project', lookup_expr='isnull', label='본사')

    class Meta:
        model = Post
        fields = ('company', 'project', 'board', 'is_notice', 'is_com', 'category', 'lawsuit')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_class = PostFilterSet
    search_fields = ('title', 'content', 'user__username')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class LikeViewSet(viewsets.ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     filterset_fields = ('user', 'post')
#
#
# class DisLikeViewSet(viewsets.ModelViewSet):
#     queryset = DisLike.objects.all()
#     serializer_class = DisLikeSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     filterset_fields = ('user', 'post')


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
