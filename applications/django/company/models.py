from django.db import models
from django.urls import reverse


class Company(models.Model):
    name = models.CharField('회사명', max_length=100)
    tax_number = models.CharField('사업자등록번호', max_length=12)
    ceo = models.CharField('대표자명', max_length=30)
    org_number = models.CharField('법인등록번호', max_length=14)
    business_cond = models.CharField('업태', max_length=20, blank=True)
    business_even = models.CharField('종목', max_length=20, blank=True)
    es_date = models.DateField('설립일자', null=True, blank=True)
    op_date = models.DateField('개업일자', null=True, blank=True)
    zipcode = models.CharField('우편번호', max_length=5, blank=True)
    address1 = models.CharField('주소', max_length=50, blank=True)
    address2 = models.CharField('상세주소', max_length=30, blank=True)
    address3 = models.CharField('참고항목', max_length=30, blank=True)

    class Meta:
        verbose_name = "01. 회사 정보"
        verbose_name_plural = "01. 회사 정보"
        db_table = 'rebs_company'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rebs:company:update', args=(self.pk,))


class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField('부서명', max_length=20)
    task = models.CharField('주요 업무', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = '02. 부서 정보'
        verbose_name_plural = '02. 부서 정보'


class Staff(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name='부서 정보',
                                   related_name='staffs')
    position = models.CharField('직함', max_length=50, blank=True, default='')
    name = models.CharField('직원 성명', max_length=10)
    birth_date = models.DateField('생년월일')
    GENDER_CHOICES = (('M', '남성'), ('F', '여성'))
    gender = models.CharField('성별', max_length=1, choices=GENDER_CHOICES)
    entered_date = models.DateField('입사일')
    personal_phone = models.CharField('휴대전화', max_length=13, blank=True)
    email = models.EmailField('이메일', null=True, blank=True)
    STATUS_CHOICES = (('1', '근무 중'), ('2', '정직 중'), ('3', '퇴사신청'), ('4', '퇴사처리'))
    status = models.CharField('상태', max_length=1, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return f'{self.name}({self.birth_date})'

    class Meta:
        verbose_name = '03. 직원 정보'
        verbose_name_plural = '03. 직원 정보'
