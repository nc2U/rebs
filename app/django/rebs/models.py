from django.db import models


class AccountSort(models.Model):
    name = models.CharField(max_length=2)
    accounts = models.ManyToManyField('rebs.AccountSubD1')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "00. 본사계정 구분"
        verbose_name_plural = "00. 본사계정 구분"


class AccountSubD1(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=20)

    def __str__(self):
        return f'[{self.code}] {self.name} 계정'

    class Meta:
        ordering = ['id']
        verbose_name = "01. 계정과목 (대분류)"
        verbose_name_plural = "01. 계정과목 (대분류)"


class AccountSubD2(models.Model):
    d1 = models.ForeignKey(AccountSubD1, on_delete=models.CASCADE, related_name='acc_d2s')
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    def __str__(self):
        return f'[{self.code}] {self.name}'

    class Meta:
        ordering = ['id']
        verbose_name = "02. 계정과목 (중분류)"
        verbose_name_plural = "02. 계정과목 (중분류)"


class AccountSubD3(models.Model):
    d2 = models.ForeignKey(AccountSubD2, on_delete=models.CASCADE, related_name='acc_d3s')
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=20)
    is_special = models.BooleanField(default=False)
    description = models.CharField(max_length=50)

    def __str__(self):
        return f'[{self.code}] {self.name}'

    class Meta:
        ordering = ['id']
        verbose_name = "03. 계정과목 (소분류)"
        verbose_name_plural = "03. 계정과목 (소분류)"


class ProjectAccountSort(models.Model):
    name = models.CharField(max_length=2)
    accounts = models.ManyToManyField('rebs.ProjectAccountD1')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "04. 현장계정 구분"
        verbose_name_plural = "04. 현장계정 구분"


class ProjectAccountD1(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = "05. 프로젝트 계정"
        verbose_name_plural = "05. 프로젝트 계정"


class ProjectAccountD2(models.Model):
    d1 = models.ForeignKey(ProjectAccountD1, on_delete=models.CASCADE, related_name='acc_d2s')
    code = models.CharField(max_length=3)
    sub_title = models.CharField(max_length=20, blank=True, help_text='중분류 항목이 존재할 경우 기재')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = "06. 프로젝트 세부계정"
        verbose_name_plural = "06. 프로젝트 세부계정"


class WiseSaying(models.Model):
    saying_ko = models.CharField(max_length=300)
    saying_en = models.CharField(max_length=300)
    spoked_by = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.saying_ko} - {self.spoked_by}'

    class Meta:
        verbose_name = "오늘의 한마디"
        verbose_name_plural = "오늘의 한마디"
