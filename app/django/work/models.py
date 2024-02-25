import hashlib

from datetime import datetime

from django.db import models

from project.models import Project


class TaskProject(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, verbose_name="회사")
    name = models.CharField('이름', max_length=100)
    desc = models.TextField('설명', blank=True, default='')
    identifier = models.CharField('식별자', max_length=100, unique=True,
                                  help_text='1에서 100글자 소문자(a-z), 숫자, 대쉬(-)와 밑줄(_)만 가능합니다. 식별자는 저장 후에는 수정할 수 없습니다.')
    homepage = models.URLField('홈페이지', max_length=255, null=True, blank=True)
    is_public = models.BooleanField('공개', default=True, help_text='공개 프로젝트는 모든 로그인한 사용자가 접속할 수 있습니다.')
    parent_project = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='상위 프로젝트')
    depth = models.PositiveSmallIntegerField('단계', default=1,
                                             help_text='프로젝트 간 상하 소속 관계에 의한 단계, 최상위인 경우 1단계 이후 각 뎁스 마다 1씩 증가')
    is_inherit_members = models.BooleanField('상위 프로젝트 멤버 상속', default=False)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='사용자')
    created = models.DateTimeField('생성일시', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created',)
        verbose_name = '01. 프로젝트(업무)'
        verbose_name_plural = '01. 프로젝트(업무)'


class Module(models.Model):
    project = models.ForeignKey(TaskProject, on_delete=models.CASCADE, verbose_name='프로젝트')
    issue = models.BooleanField('업무관리', default=True)
    time = models.BooleanField('시간추적', default=True)
    news = models.BooleanField('공지', default=True)
    document = models.BooleanField('문서', default=True)
    file = models.BooleanField('파일', default=True)
    wiki = models.BooleanField('위키', default=True)
    repository = models.BooleanField('저장소', default=True)
    forum = models.BooleanField('게시판', default=True)
    calendar = models.BooleanField('달력', default=True)
    gantt = models.BooleanField('Gantt 차트', default=True)

    def __str__(self):
        return self.issue


class Version(models.Model):
    project = models.ForeignKey(TaskProject, on_delete=models.CASCADE, verbose_name='프로젝트')
    name = models.CharField('이름', max_length=20)
    desc = models.CharField('설명', max_length=255, blank=True, default='')
    status = models.CharField('상태', max_length=1, choices=(('1', '진행'), ('2', '잠김'), ('3', '닫힘')), default='1')
    wiki_page = models.CharField('위키 페이지', max_length=255, blank=True, null=True)
    release_date = models.DateField(verbose_name='출시일', blank=True, null=True)
    SHARE_CHOICES = (
        ('0', '공유 없음'), ('1', '하위 프로젝트'), ('2', '상위 및 하위 프로젝트'), ('3', '최상위 및 모든 하위 프로젝트'), ('4', '모든 프로젝트'))
    share = models.CharField('공유', max_length=1, default='0')
    is_default = models.BooleanField('기본 버전', default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class TaskCategory(models.Model):
    project = models.ForeignKey(TaskProject, on_delete=models.CASCADE, verbose_name='프로젝트')
    name = models.CharField('범주', max_length=100)
    assignee = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='담당자')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class Repository(models.Model):
    project = models.ForeignKey(TaskProject, on_delete=models.CASCADE, verbose_name='프로젝트')
    SCM_CHOICES = (('1', 'Git'),)
    scm = models.CharField('종류', max_length=10, default='1')
    is_default = models.BooleanField('주저장소', default=True)
    identifier = models.CharField('식별자', max_length=20, unique=True, blank=True, null=True,
                                  help_text='1 에서 255 글자 소문자(a-z),숫자,대쉬(-)와 밑줄(_)만 가능합니다. 식별자는 저장후에는 수정할 수 없습니다.')
    path = models.CharField('저장소 경로', max_length=255, help_text='로컬의 bare 저장소 (예: //gitrepo, c:\\gitrepo)')
    path_encoding = models.CharField('경로 인코딩', max_length=20, default='UTF-8', help_text='기본: UTF-8')
    is_report = models.BooleanField('파일이나 폴더의 마지막 커밋을 보고', default=False)

    def __str__(self):
        return self.scm

    class Meta:
        ordering = ('id',)


class Member(models.Model):
    project = models.ForeignKey(TaskProject, on_delete=models.CASCADE, verbose_name='프로젝트')
    member = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='구성원')
    roles = models.ManyToManyField('Role', verbose_name='역할')

    def __str__(self):
        return self.member

    class Meta:
        verbose_name = '02. 구성원'
        verbose_name_plural = '02. 구성원'


class Role(models.Model):
    name = models.CharField('이름', max_length=20)
    can_task_assign = models.BooleanField('업무 위탁 권한', default=True)
    TASK_VIEW_PERM = (('ALL', '모든 업무'), ('PUB', '비공개 업무 제외'), ('PRI', '직접 생성 또는 담당한 업무'))
    task_visible = models.CharField('업무 보기 권한', max_length=3, choices=TASK_VIEW_PERM, default='PUB')
    TIME_VIEW_PERM = (('ALL', '모든 시간기록'), ('PRI', '직접 생성한 시간기록'))
    time_log_visible = models.CharField('시간기록 보기 권한', max_length=3, choices=TIME_VIEW_PERM, default='ALL')
    USER_VIEW_PERM = (('ALL', '모든 활성 사용자'), ('PRJ', '보이는 프로젝트 사용자'))
    user_visible = models.CharField('사용자 보기 권한', max_length=3, choices=USER_VIEW_PERM, default='ALL')
    default_time_activity = models.ForeignKey('CodeActivity', on_delete=models.SET_NULL, null=True, blank=True,
                                              verbose_name='기본 활동')
    order = models.PositiveSmallIntegerField('정렬', default=1)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='사용자')
    created = models.DateTimeField('생성일시', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order', 'created',)
        verbose_name = '03. 역할 및 권한'
        verbose_name_plural = '03. 역할 및 권한'


class Permission(models.Model):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    # 프로젝트
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
    # 게시판
    forum_read = models.BooleanField('게시물 보기', default=True)
    forum_create = models.BooleanField('게시물 추가', default=True)
    forum_update = models.BooleanField('게시물 편집', default=False)
    forum_own_update = models.BooleanField('내 게시물 편집', default=True)
    forum_delete = models.BooleanField('게시물 삭제', default=False)
    forum_own_delete = models.BooleanField('내 게시물 삭제', default=False)
    forum_watcher_read = models.BooleanField('게시물 관람자 보기', default=False)
    forum_watcher_create = models.BooleanField('게시물 관람자 추가', default=False)
    forum_watcher_delete = models.BooleanField('게시물 관람자 삭제', default=False)
    forum_manage = models.BooleanField('게시판 관리', default=False)
    # 달력
    calendar_read = models.BooleanField('달력 보기', default=True)
    # 문서
    document_read = models.BooleanField('문서 보기', default=True)
    document_create = models.BooleanField('문서 추가', default=False)
    document_update = models.BooleanField('문서 편집', default=False)
    document_delete = models.BooleanField('문서 삭제', default=False)
    # 파일
    file_read = models.BooleanField('파일 보기', default=True)
    file_manage = models.BooleanField('파일 관리', default=False)
    # 간트차트
    gantt_read = models.BooleanField('간트 차트 보기', default=True)
    # 업무
    task_read = models.BooleanField('업무 보기', default=True)
    task_create = models.BooleanField('업무 추가', default=True)
    task_update = models.BooleanField('업무 편집', default=False)
    task_own_update = models.BooleanField('내 업무 편집', default=True)
    task_copy = models.BooleanField('업무 복사', default=True)
    task_rel_manage = models.BooleanField('업무 관계 관리', default=True)
    task_sub_manage = models.BooleanField('하위 업무 관리', default=True)
    task_public = models.BooleanField('업무 공개/비공개 설정', default=False)
    task_own_public = models.BooleanField('내 업무 공개/비공개 설정', default=True)
    task_comment_create = models.BooleanField('댓글 추가', default=True)
    task_comment_update = models.BooleanField('댓글 편집', default=False)
    task_comment_own_update = models.BooleanField('내 댓글 편집', default=True)
    task_private_comment_read = models.BooleanField('비공개 댓글 보기', default=False)
    task_private_comment_set = models.BooleanField('댓글 비공개로 설정', default=False)
    task_delete = models.BooleanField('업무 삭제', default=False)
    task_watcher_read = models.BooleanField('업무 관람자 보기', default=False)
    task_watcher_create = models.BooleanField('업무 관람자 추가', default=False)
    task_watcher_delete = models.BooleanField('업무 관람자 삭제', default=False)
    task_import = models.BooleanField('업무 가져오기', default=False)
    task_category_manage = models.BooleanField('업무 범주 관리', default=False)
    # 공지(뉴스)
    news_read = models.BooleanField('공지 보기', default=True)
    news_manage = models.BooleanField('공지 관리', default=False)
    news_comment = models.BooleanField('공지 댓글 달기', default=True)
    # 저장소(레파지토리)
    repo_changesets_read = models.BooleanField('변경 묶음 보기', default=False)
    repo_read = models.BooleanField('저장소 보기', default=False)
    repo_commit_access = models.BooleanField('변경 로그 보기', default=False)
    repo_rel_task_manage = models.BooleanField('연결된 업무 관리', default=False)
    repo_manage = models.BooleanField('저장소 관리', default=False)
    # 시간추적
    time_read = models.BooleanField('시간 입력 보기', default=True)
    time_create = models.BooleanField('작업 시간 기록', default=True)
    time_update = models.BooleanField('시간 입력 편집', default=False)
    time_own_update = models.BooleanField('내 시간 입력 편집', default=True)
    time_pro_act_manage = models.BooleanField('프로젝트 작업내역 관리', default=False)
    time_other_user_log = models.BooleanField('다른 사용자 소요시간 입력', default=False)
    time_entries_import = models.BooleanField('소요시간 가져오기', default=False)
    # 위키
    wiki_read = models.BooleanField('위키 보기', default=True)
    wiki_history_read = models.BooleanField('위키 기록 보기', default=True)
    wiki_page_export = models.BooleanField('위키 페이지 내보내기', default=False)
    wiki_page_update = models.BooleanField('위키 페이지 편집', default=False)
    wiki_page_rename = models.BooleanField('위키 페이지 이름변경', default=False)
    wiki_page_delete = models.BooleanField('위키 페이지 삭제', default=False)
    wiki_attachment_delete = models.BooleanField('첨부파일 삭제', default=False)
    wiki_watcher_read = models.BooleanField('위키 관람자 보기', default=False)
    wiki_watcher_create = models.BooleanField('위키 관람자 추가', default=False)
    wiki_watcher_delete = models.BooleanField('위키 관람자 삭제', default=False)
    wiki_page_project = models.BooleanField('프로젝트 위키 페이지', default=False)
    wiki_manage = models.BooleanField('위키 관리', default=False)

    def __str__(self):
        return f'{self.role.name} - 권한'


class Tracker(models.Model):
    name = models.CharField('이름', max_length=100)
    default_status = models.ForeignKey('Status', on_delete=models.PROTECT, verbose_name='초기 상태')
    displayed = models.BooleanField('로드맵에 표시', default=True)
    desc = models.CharField('설명', max_length=255, blank=True, default='')
    projects = models.ManyToManyField(TaskProject, blank=True, verbose_name='프로젝트')
    order = models.PositiveSmallIntegerField('정렬', default=1)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='사용자')
    created = models.DateTimeField('생성일시', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order', 'created')
        verbose_name = '04. 업무 유형'
        verbose_name_plural = '04. 업무 유형'


class Status(models.Model):
    name = models.CharField('이름', max_length=20)
    desc = models.CharField('설명', max_length=255, blank=True, default='')
    closed = models.BooleanField('완료 상태', default=False)
    order = models.PositiveSmallIntegerField('정렬', default=1)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='사용자')
    created = models.DateTimeField('생성일시', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order', 'created',)
        verbose_name = '05. 업무 상태'
        verbose_name_plural = '05. 업무 상태'


class Workflow(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='역할')
    tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE, verbose_name='업무 유형')
    status = models.OneToOneField(Status, on_delete=models.CASCADE, verbose_name='업무 상태',
                                  related_name='each_status')
    statuses = models.ManyToManyField(Status, verbose_name='허용 업무 상태', blank=True)

    def __str__(self):
        return f'{self.role} - {self.tracker}'

    class Meta:
        verbose_name = '06. 업무 흐름'
        verbose_name_plural = '06. 업무 흐름'


class CodeActivity(models.Model):
    name = models.CharField('이름', max_length=50)
    active = models.BooleanField('사용중', default=True)
    default = models.BooleanField('기본값', default=False)
    order = models.PositiveSmallIntegerField('정렬', default=1)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='사용자')
    created = models.DateTimeField('생성일시', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order', 'created',)
        verbose_name = '07. 작업분류(시간추적)'
        verbose_name_plural = '07. 작업분류(시간추적)'


class CodeIssuePriority(models.Model):
    name = models.CharField('이름', max_length=20)
    active = models.BooleanField('사용중', default=True)
    default = models.BooleanField('기본값', default=False)
    order = models.PositiveSmallIntegerField('정렬', default=1)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='사용자')
    created = models.DateTimeField('생성일시', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order', 'created',)
        verbose_name = '08. 업무 우선순위'
        verbose_name_plural = '08. 업무 우선순위'


class CodeDocsCategory(models.Model):
    name = models.CharField('이름', max_length=20)
    active = models.BooleanField('사용중', default=True)
    default = models.BooleanField('기본값', default=False)
    order = models.PositiveSmallIntegerField('정렬', default=1)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='사용자')
    created = models.DateTimeField('생성일시', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order', 'created',)
        verbose_name = '09. 문서 범주'
        verbose_name_plural = '09. 문서 범주'


class Issue(models.Model):
    project = models.ForeignKey(TaskProject, on_delete=models.PROTECT, verbose_name='프로젝트')
    tracker = models.ForeignKey(Tracker, on_delete=models.PROTECT, verbose_name='유형')
    private = models.BooleanField('비공개', default=False)
    subject = models.CharField(max_length=100, verbose_name='주제')
    desc = models.TextField(verbose_name='설명', blank=True, default='')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='상태')
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='상위업무')
    priority = models.ForeignKey(CodeIssuePriority, on_delete=models.PROTECT, verbose_name='우선순위')
    assignee = models.ForeignKey('accounts.User', on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='담당자', related_name='assignees')
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='범주')
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='버전')
    start_date = models.DateField('시작 일자', null=True, blank=True)
    due_date = models.DateField('완료 기한', null=True, blank=True)
    estimated_time = models.PositiveSmallIntegerField('추정 소요시간', null=True, blank=True)
    PROGRESS_RATIO = (
        (0.0, '0%'), (0.1, '10%'), (0.2, '20%'), (0.3, '30%'), (0.4, '40%'), (0.5, '50%'),
        (0.6, '60%'), (0.7, '70%'), (0.8, '80%'), (0.9, '90%'), (1.0, '100%'))
    progress = models.DecimalField('진척도', max_digits=2, decimal_places=1, choices=PROGRESS_RATIO, default=0.0)
    watchers = models.ManyToManyField('accounts.User', blank=True,
                                      verbose_name='업무 관람자', related_name='watchers')
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='사용자')
    created = models.DateTimeField('생성', auto_now_add=True)
    updated = models.DateTimeField('변경', auto_now=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ('-created',)
        verbose_name = '10. 업무(작업)'
        verbose_name_plural = '10. 업무(작업)'


def get_file_name(filename):
    file = filename.split('.')
    ext = file.pop()
    year = datetime.today().strftime('%Y')
    month = datetime.today().strftime('%m')
    day = datetime.today().strftime('%d')
    h = hashlib.blake2b(digest_size=3)
    h.update(bytes(f'{datetime.now().timestamp()}', 'utf-8'))
    return f"{year}/{month}/{year}{month}{day}_{h.hexdigest()}_{''.join(file)}.{ext}"


def get_file_path(instance, filename):
    return f"task/{get_file_name(filename)}"


class IssueFile(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, default=None, verbose_name='업무', related_name='files')
    file = models.FileField(upload_to='files', verbose_name='파일')
    desc = models.CharField('부가설명', max_length=255, blank=True, default='')

    def __str__(self):
        return self.file


class IssueComment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, verbose_name='업무', related_name='comments')
    content = models.TextField('내용')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='사용자')
    created = models.DateTimeField('생성일시', auto_now_add=True)
    updated = models.DateTimeField('수정일시', auto_now=True)

    def __str__(self):
        return self.content


class SpentTime(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, verbose_name='업무')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='사용자')
    date = models.DateField(verbose_name='작업일자')
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.CharField('설명', max_length=255, blank=True, default='')
    activity = models.ForeignKey(CodeActivity, on_delete=models.PROTECT, verbose_name='작업분류(시간추적)')

    def __str__(self):
        return self.hours

    class Meta:
        ordering = ('date',)
