from django_filters import BooleanFilter
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets

from ..pagination import PageNumberPaginationThreeThousand
from ..permission import *
from ..serializers.document import *


# Document --------------------------------------------------------------------------

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)
    filterset_fields = ('group', 'search_able', 'manager')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)
    filterset_fields = ('board',)


class LawSuitCaseFilterSet(FilterSet):
    is_com = BooleanFilter(field_name='project', lookup_expr='isnull', label='본사')
    in_progress = BooleanFilter(field_name='case_end_date', lookup_expr='isnull', label='진행중')

    class Meta:
        model = LawsuitCase
        fields = ('company', 'is_com', 'project', 'sort', 'level', 'court', 'in_progress')


class LawSuitCaseBase(viewsets.ModelViewSet):
    queryset = LawsuitCase.objects.all()
    serializer_class = LawSuitCaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)
    filterset_class = LawSuitCaseFilterSet
    search_fields = ('other_agency', 'case_number', 'case_name',
                     'plaintiff', 'defendant', 'case_start_date',
                     'case_end_date', 'summary')

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
        fields = ('company', 'project', 'is_com', 'board', 'is_notice', 'category', 'lawsuit')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)
    filterset_class = PostFilterSet
    search_fields = (
        'lawsuit__case_number', 'lawsuit__case_name', 'title',
        'content', 'links__link', 'files__file', 'user__username')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('post', 'user')


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)


class CommentFilterSet(FilterSet):
    is_comment = BooleanFilter(field_name='parent', lookup_expr='isnull', label='댓글')

    class Meta:
        model = Comment
        fields = ('user', 'post', 'is_comment')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)
    filterset_class = CommentFilterSet

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('comment', 'user')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)
