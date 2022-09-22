from rest_framework import viewsets

from ..permission import *
from ..serializers.document import *

from document.models import (Group, Board, Category, LawsuitCase, Post,
                             Like, DisLike, Image, Link, File, Comment, Tag)


# Document --------------------------------------------------------------------------

class GroupViewSets(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BoardViewSets(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('group', 'search_able', 'manager')


class CategoryViewSets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('board',)


class LawSuitCaseViewSets(viewsets.ModelViewSet):
    queryset = LawsuitCase.objects.all()
    serializer_class = LawSuitCaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project', 'sort', 'level', 'court')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('board', 'is_notice', 'project', 'category', 'lawsuit')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSets(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('user', 'post')


class DisLikeViewSets(viewsets.ModelViewSet):
    queryset = DisLike.objects.all()
    serializer_class = DisLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('user', 'post')


class ImageViewSets(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class LinkViewSets(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class FileViewSets(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CommentViewSets(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSets(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
