from rest_framework import generics, viewsets

from ..permission import *
from ..serializers.document import *

from document.models import Group, Board, Category, LawsuitCase, Post, Image, Link, File, Comment, Tag


# Document --------------------------------------------------------------------------
class GroupList(generics.ListCreateAPIView):
    name = 'group-list'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'group-detail'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BoardList(generics.ListCreateAPIView):
    name = 'board-list'
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'board-detail'
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CategoryList(generics.ListCreateAPIView):
    name = 'category-list'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'category-detail'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class LawSuitCaseList(generics.ListCreateAPIView):
    name = 'suitcase-list'
    queryset = LawsuitCase.objects.all()
    serializer_class = LawSuitCaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LawSuitCaseDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'suitcase-detail'
    queryset = LawsuitCase.objects.all()
    serializer_class = LawSuitCaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class PostList(generics.ListCreateAPIView):
    name = 'post-list'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'post-detail'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ImageList(generics.ListCreateAPIView):
    name = 'image-list'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'image-detail'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class LinkList(generics.ListCreateAPIView):
    name = 'link-list'
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'link-detail'
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class FileList(generics.ListCreateAPIView):
    name = 'file-list'
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'file-detail'
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CommentList(generics.ListCreateAPIView):
    name = 'comment-list'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'comment-detail'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class TagList(generics.ListCreateAPIView):
    name = 'tag-list'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'tag-detail'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
