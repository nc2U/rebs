import hashlib
from django.db import models

from accounts.models import User
from project.models import Project


class Company(models.Model):
    name = models.CharField('회사명', max_length=30, unique=True)
    tax_number = models.CharField('사업자등록번호', max_length=12)
    ceo = models.CharField('대표자명', max_length=20)
    org_number = models.CharField('법인등록번호', max_length=14)
    business_cond = models.CharField('업태', max_length=20, blank=True)
    business_even = models.CharField('종목', max_length=20, blank=True)
    es_date = models.DateField('설립일자', null=True, blank=True)
    op_date = models.DateField('개업일자', null=True, blank=True)
    zipcode = models.CharField('우편번호', max_length=5, blank=True)
    address1 = models.CharField('주소', max_length=35, blank=True)
    address2 = models.CharField('상세주소', max_length=20, blank=True)
    address3 = models.CharField('참고항목', max_length=20, blank=True)

    class Meta:
        verbose_name = "01. 회사 정보"
        verbose_name_plural = "01. 회사 정보"

    def __str__(self):
        return self.name


def get_image_filename(instance, filename):
    company = instance.company.pk
    hash_value = hashlib.md5().hexdigest()
    return f"company/{company}_{hash_value}_{filename}"


class Logo(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    generic_logo = models.ImageField(upload_to=get_image_filename, null=True, help_text='4.5:1 ~ 5:1 크기 추천',
                                     verbose_name='일반 로고')
    dark_logo = models.ImageField(upload_to=get_image_filename, null=True, help_text='4.5:1 ~ 5:1 크기 추천',
                                  verbose_name='다크 로고')
    simple_logo = models.ImageField(upload_to=get_image_filename, null=True, help_text='1:1 크기 추천',
                                    verbose_name='심플 로고')


class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments', verbose_name='회사')
    upper_depart = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='sub_departs',
                                     verbose_name='상위 부서')
    level = models.PositiveSmallIntegerField('레벨', help_text='부서 간 상하 소속 관계에 의한 단계, 최상위 부서인 경우 1단계 이후 각 뎁스 마다 1씩 증가')
    name = models.CharField('부서', max_length=30)
    task = models.CharField('주요 업무', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = '02. 부서 정보'
        verbose_name_plural = '02. 부서 정보'


class JobGrade(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ranks', verbose_name='회사')
    name = models.CharField('직급', max_length=10)
    promotion_period = models.PositiveSmallIntegerField('승급표준년수', null=True, blank=True)
    criteria_new = models.CharField('신입부여 기준', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "03. 직급 정보"
        verbose_name_plural = "03. 직급 정보"


class Position(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='positions', verbose_name='회사')
    name = models.CharField('직위', max_length=30)
    grades = models.ManyToManyField(JobGrade, related_name='positions', verbose_name='직책')
    desc = models.CharField('설명', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "04. 직위 정보"
        verbose_name_plural = "04. 직위 정보"


class DutyTitle(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='titles', verbose_name='회사')
    name = models.CharField('직책', max_length=5)
    desc = models.CharField('설명', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "05. 직책 정보"
        verbose_name_plural = "05. 직책 정보"


class Staff(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='staffs', verbose_name='회사')
    SORT_CHOICES = (('1', '임원'), ('2', '직원'))
    sort = models.CharField('구분', max_length=1, choices=SORT_CHOICES, default='1')
    name = models.CharField('직원 성명', max_length=10)
    id_number = models.CharField('주민등록번호', max_length=14)
    personal_phone = models.CharField('휴대전화', max_length=13)
    email = models.EmailField('이메일', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='부서 정보',
                                   related_name='staffs')
    grade = models.ForeignKey(JobGrade, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='직급 정보')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='직위 정보')
    duty = models.ForeignKey(DutyTitle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='직책 정보')
    date_join = models.DateField('입사일')
    STATUS_CHOICES = (('1', '근무 중'), ('2', '휴직 중'), ('3', '퇴직신청'), ('4', '퇴사처리'))
    status = models.CharField('상태', max_length=1, choices=STATUS_CHOICES, default='1')
    date_leave = models.DateField('퇴사일', null=True, blank=True)
    user = models.OneToOneField('accounts.User', on_delete=models.DO_NOTHING, null=True, blank=True,
                                verbose_name='유저 정보')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_join']
        verbose_name = '06. 직원 정보'
        verbose_name_plural = '06. 직원 정보'

# class Role(models.Model):
#     name = models.CharField('이름')
#
#     def __str__(self):
#         return self.name
#
#
# class Permission(models.Model):
#     name = models.CharField('이름')
#
#     def __str__(self):
#         return self.name
#
#
# class WorkType(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='회사')
#     name = models.CharField('유형', max_length=100)
#     order = models.PositiveSmallIntegerField('정렬 순서', default=0)
#
#     def __str__(self):
#         return self.name
#
#
# class WorkProject(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='회사')
#     title = models.CharField('이름', max_length=100)
#     desc = models.TextField('설명', null=True, blank=True)
#     identifier = models.CharField('식별자', max_length=20)
#     is_public = models.BooleanField('공개여부', default=False)
#     work_types = models.ManyToManyField(WorkType, verbose_name='작업 유형', blank=True)
#
#
# class WorkCate(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='회사')
#     name = models.CharField('범주', max_length=100)
#     order = models.PositiveSmallIntegerField('정렬 순서', default=0)
#
#     def __str__(self):
#         return self.name
#
#
# class Work(models.Model):
#     type = models.ForeignKey(WorkType, on_delete=models.PROTECT, verbose_name='유형')
#     title = models.CharField(max_length=100, verbose_name='업무 제목')
#     desc = models.TextField(verbose_name='설명', blank=True, default='')
#     WORK_STATUS = (('0', '신규'), ('1', '진행'), ('2', '해결'), ('3', '의견'), ('4', '완료'), ('5', '거절'))
#     status = models.CharField('상태', max_length=1, choices=WORK_STATUS, default='0')
#     upper_work = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, verbose_name='상위 업무')
#     cate = models.ForeignKey(WorkCate, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='범주')
#     is_secret = models.BooleanField('비공개', default=False)
#     WORK_PRIORITY = (('1', '낮음'), ('2', '보통'), ('3', '높음'), ('4', '긴급'), ('5', '즉시'))
#     priority = models.CharField('우선 순위', max_length=1, choices=WORK_PRIORITY)
#     worker = models.OneToOneField('accounts.User', on_delete=models.PROTECT, verbose_name='담당자')
#     start_time = models.DateTimeField('시작 시간', null=True, blank=True)
#     deadline = models.DateTimeField('완료 기한', null=True, blank=True)
#     WORK_PROGRESS = (
#         ('0', '0%'), ('1', '10%'), ('2', '20%'), ('3', '30%'), ('4', '40%'), ('5', '50%'),
#         ('6', '60%'), ('7', '70%'), ('8', '80%'), ('9', '90%'), ('10', '100%'))
#     progress = models.CharField('진척도', max_length=1, choices=WORK_PROGRESS)
#     done_time = models.DateTimeField('완료 일시', null=True, blank=True)
#     collaborator = models.ManyToManyField('accounts.User', null=True, blank=True, verbose_name='업무협력자')
#     user = models.ForeignKey('accounts.User', on_delete=models.PROTECT, verbose_name='업무 생성자')
#     created = models.DateTimeField('생성일', auto_now_add=True)
#
#
# class WorkFile(models.Model):
#     work = models.OneToOneField('Work', on_delete=models.PROTECT, verbose_name='파일')
#     desc = models.CharField('부가설명', max_length=255, blank=True, default='')
#
#
# class WorkComment(models.Model):
#     work = models.ForeignKey(Work, related_name='comments', on_delete=models.CASCADE)
#     comment = models.TextField('')
#     user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
#     created = models.DateTimeField('생성일시', auto_now_add=True)
#     updated = models.DateTimeField('수정일시', auto_now=True)
