from django.db import models

# class WorkProject(models.Model):
#     company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
#     title = models.CharField('이름', max_length=100)
#     desc = models.TextField('설명', blank=True, default='')
#     identifier = models.CharField('식별자', max_length=20, unique=True)
#     homepage = models.URLField('홈페이지')

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
