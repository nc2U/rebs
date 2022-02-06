from django.db import models


class Company(models.Model):
    name = models.CharField('회사명', max_length=100, unique=True)
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

    def __str__(self):
        return self.name


class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments', verbose_name='회사')
    upper_depart = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='sub_departs',
                                     verbose_name='상위 부서')
    name = models.CharField('부서', max_length=20)
    task = models.CharField('주요 업무', max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = '02. 부서 정보'
        verbose_name_plural = '02. 부서 정보'


class Position(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='positions', verbose_name='회사')
    SORT_CHOICES = (('1', '임원'), ('2', '직원'))
    sort = models.CharField('구분', max_length=1, choices=SORT_CHOICES)
    rank = models.CharField('직책', max_length=20)
    title = models.CharField('직함', max_length=20, blank=True)
    description = models.CharField('설명', max_length=255, blank=True)

    def __str__(self):
        return self.rank

    class Meta:
        ordering = ['id']
        verbose_name = "03. 직책 정보"
        verbose_name_plural = "03. 직책 정보"


class Staff(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.DO_NOTHING, null=True, blank=True,
                                verbose_name='유저 정보')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='부서 정보',
                                   related_name='staffs')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='직책 정보')
    name = models.CharField('직원 성명', max_length=10)
    birth_date = models.DateField('생년월일', null=True, blank=True)
    GENDER_CHOICES = (('M', '남성'), ('F', '여성'))
    gender = models.CharField('성별', max_length=1, choices=GENDER_CHOICES, blank=True)
    entered_date = models.DateField('입사일')
    personal_phone = models.CharField('휴대전화', max_length=13)
    email = models.EmailField('이메일')
    STATUS_CHOICES = (('1', '근무 중'), ('2', '정직 중'), ('3', '퇴사신청'), ('4', '퇴사처리'))
    status = models.CharField('상태', max_length=1, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return f'{self.name}({self.birth_date})'

    class Meta:
        ordering = ['-entered_date']
        verbose_name = '04. 직원 정보'
        verbose_name_plural = '04. 직원 정보'
