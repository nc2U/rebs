from datetime import datetime

from django_filters import BooleanFilter
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, status
from rest_framework.response import Response

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
        fields = ('company', 'project', 'is_com', 'board', 'is_notice', 'category', 'lawsuit', 'user')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(deleted=None)
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)
    filterset_class = PostFilterSet
    search_fields = (
        'lawsuit__case_number', 'lawsuit__case_name', 'title',
        'content', 'links__link', 'files__file', 'user__username')

    def copy_and_create(self, request, *args, **kwargs):
        # 복사할 행의 ID를 저장한다.
        origin_pk = kwargs.get('pk')
        project = request.data.get('project')
        board = request.data.get('board')

        try:
            # 기존 행을 가져와서 복사한다.
            org_instance = Post.objects.get(pk=origin_pk)

            add_text = f'<br /><br /><p>[이 게시물은 {self.request.user.username} 님에 의해 {datetime.now()} {org_instance.board.name} 에서 복사됨]</p>'

            # 기존 행의 정보를 사용하여 새로운 행을 생성한다.
            new_instance_data = {
                'company': org_instance.company.pk,
                'project': project if project else None,
                'board': board,
                'category': org_instance.category.pk if org_instance.category else None,
                'lawsuit': org_instance.lawsuit.pk if org_instance.lawsuit else None,
                'title': org_instance.title,
                'execution_date': org_instance.execution_date if org_instance.execution_date else None,
                'content': org_instance.content + add_text,
            }

            # Serializer를 사용해 새로운 행을 생성하고 저장한다.
            serializer = PostSerializer(data=new_instance_data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({'detail': 'Original Post object does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PostBlameViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostBlameSerializer
    permission_classes = (permissions.IsAuthenticated,)


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
        fields = ('user', 'post', 'is_comment', 'user')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_class = CommentFilterSet

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CommentBlameViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentBlameSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsProjectStaffOrReadOnly)


class PostInTrashViewSet(PostViewSet):
    queryset = Post.objects.filter(deleted__isnull=False)
    serializer_class = PostInTrashSerializer
