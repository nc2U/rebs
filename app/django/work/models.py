from django.db import models


class TaskProject(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    name = models.CharField('이름', max_length=100)
    desc = models.TextField('설명', blank=True, default='')
    identifier = models.CharField('식별자', max_length=100, unique=True,
                                  help_text='1에서 100글자 소문자(a-z), 숫자, 대쉬(-)와 밑줄(_)만 가능합니다. 식별자는 저장 후에는 수정할 수 없습니다.')
    homepage = models.URLField('홈페이지', max_length=200, null=True, blank=True)
    public = models.BooleanField('공개', default=True, help_text='공개 프로젝트는 모든 로그인한 사용자가 접속할 수 있습니다.')
    parent_project = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    inherit_members = models.BooleanField('상위 프로젝트 멤버 상속', default=False)
    members = models.ManyToManyField('accounts.User')


class Role(models.Model):
    name = models.CharField('이름', max_length=20)
    can_task_assign = models.BooleanField('작업 위탁 가능', default=True)
    TASK_VIEW_PERM = (('ALL', '모든 작업'), ('PUB', '비공개 작업 제외'), ('PRI', '직접 생성 또는 담당한 작업'))
    task_visible = models.CharField('작업 가시성', max_length=3, choices=TASK_VIEW_PERM, default='PUB')
    TIME_VIEW_PERM = (('ALL', '모든 시간기록'), ('PRI', '직접 생성한 시간기록'))
    time_log_visible = models.CharField('시간기록 가시성', max_length=3, choices=TIME_VIEW_PERM, default='ALL')
    USER_VIEW_PERM = (('ALL', '모든 활성 사용자'), ('PRJ', '보이는 프로젝트 사용자'))
    user_visible = models.CharField('시간기록 가시성', max_length=3, choices=TIME_VIEW_PERM, default='ALL')

    def __str__(self):
        return self.name


class Permission(models.Model):
    project_create = models.BooleanField('프로젝트 생성', default=False)
    project_update = models.BooleanField('프로젝트 편집', default=False)
    project_close = models.BooleanField('프로젝트 닫기/열기', default=False)
    project_delete = models.BooleanField('프로젝트 삭제', default=False)
    project_public = models.BooleanField('프로젝트 공개/비공개 설정', default=False)
    project_module = models.BooleanField('프로젝트 모듈 선택', default=False)
    project_member = models.BooleanField('구성원 관리', default=False)
    project_version = models.BooleanField('버전 관리', default=False)
    project_create_sub = models.BooleanField('하위 프로젝트 생성', default=False)
    project_pub_query = models.BooleanField('공용 검색양식 관리', default=False)
    project_save_query = models.BooleanField('검색양식 저장', default=True)
    forum_read = models.BooleanField('게시물 보기', default=True)
    forum_create = models.BooleanField('게시물 생성', default=True)
    forum_update = models.BooleanField('게시물 편집', default=False)
    forum_own_update = models.BooleanField('내 게시물 편집', default=False)
    forum_delete = models.BooleanField('게시물 삭제', default=False)
    forum_own_delete = models.BooleanField('내 게시물 삭제', default=False)
    forum_manage = models.BooleanField('게시판 관리', default=False)
    calendar_read = models.BooleanField('달력 보기', default=True)
    document_read = models.BooleanField('문서 보기', default=True)
    document_create = models.BooleanField('문서 생성', default=True)
    document_update = models.BooleanField('문서 편집', default=True)
    document_delete = models.BooleanField('문서 삭제', default=True)

# class TaskType(models.Model):
#     name = models.CharField('유형', max_length=100)
#     order = models.PositiveSmallIntegerField('정렬 순서', default=0)
#
#     def __str__(self):
#         return self.name
#
#
# class TaskCate(models.Model):
#     name = models.CharField('범주', max_length=100)
#     order = models.PositiveSmallIntegerField('정렬 순서', default=0)
#
#     def __str__(self):
#         return self.name
#
#
# class Task(models.Model):
#     type = models.ForeignKey(TaskType, on_delete=models.PROTECT, verbose_name='유형')
#     title = models.CharField(max_length=100, verbose_name='업무 제목')
#     desc = models.TextField(verbose_name='설명', blank=True, default='')
#     Task_STATUS = (('0', '신규'), ('1', '진행'), ('2', '해결'), ('3', '의견'), ('4', '완료'), ('5', '거절'))
#     status = models.CharField('상태', max_length=1, choices=Task_STATUS, default='0')
#     upper_Task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, verbose_name='상위 업무')
#     cate = models.ForeignKey(TaskCate, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='범주')
#     is_secret = models.BooleanField('비공개', default=False)
#     Task_PRIORITY = (('1', '낮음'), ('2', '보통'), ('3', '높음'), ('4', '긴급'), ('5', '즉시'))
#     priority = models.CharField('우선 순위', max_length=1, choices=Task_PRIORITY)
#     Tasker = models.OneToOneField('accounts.User', on_delete=models.PROTECT, verbose_name='담당자')
#     start_time = models.DateTimeField('시작 시간', null=True, blank=True)
#     deadline = models.DateTimeField('완료 기한', null=True, blank=True)
#     Task_PROGRESS = (
#         ('0', '0%'), ('1', '10%'), ('2', '20%'), ('3', '30%'), ('4', '40%'), ('5', '50%'),
#         ('6', '60%'), ('7', '70%'), ('8', '80%'), ('9', '90%'), ('10', '100%'))
#     progress = models.CharField('진척도', max_length=1, choices=Task_PROGRESS)
#     done_time = models.DateTimeField('완료 일시', null=True, blank=True)
#     collaborator = models.ManyToManyField('accounts.User', null=True, blank=True, verbose_name='업무협력자')
#     user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='업무 생성자')
#     created = models.DateTimeField('생성일', auto_now_add=True)
#
#
# class TaskFile(models.Model):
#     Task = models.OneToOneField('Task', on_delete=models.PROTECT, verbose_name='파일')
#     desc = models.CharField('부가설명', max_length=255, blank=True, default='')
#
#
# class TaskComment(models.Model):
#     Task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
#     comment = models.TextField('')
#     user = models.ForeignKey('accounts.User', related_name='comments', on_delete=models.CASCADE)
#     created = models.DateTimeField('생성일시', auto_now_add=True)
#     updated = models.DateTimeField('수정일시', auto_now=True)
