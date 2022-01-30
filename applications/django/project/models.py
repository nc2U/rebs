from django.db import models
from django.conf import settings


class Project(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT, verbose_name='회사정보')
    name = models.CharField('프로젝트명', max_length=30)
    order = models.PositiveSmallIntegerField('정렬순서', null=True, blank=True)
    KIND_CHOICES = (
        ('1', '공동주택(아파트)'),
        ('2', '공동주택(타운하우스)'),
        ('3', '주상복합(아파트)'),
        ('4', '주상복합(오피스텔)'),
        ('5', '근린생활시설'),
        ('6', '생활형숙박시설'),
        ('7', '지식산업센터'),
        ('8', '기타')
    )
    kind = models.CharField('프로젝트종류', max_length=2, choices=KIND_CHOICES)
    start_year = models.CharField('사업개시년도', max_length=4)
    is_direct_manage = models.BooleanField('직영운영여부', default=False,
                                           help_text='본사 직접 운영하는 프로젝트인 경우 체크, 즉 시행대행이나 업무대행이 아닌 경우')
    is_returned_area = models.BooleanField('토지환지여부', default=False, help_text='해당 사업부지가 환지방식 도시개발사업구역인 경우 체크')
    is_unit_set = models.BooleanField('동호지정여부', default=False, help_text='현재 동호수를 지정하지 않는 경우 체크하지 않음')
    local_zipcode = models.CharField('우편번호', max_length=5, blank=True, null=True)
    local_address1 = models.CharField('대표부지 주소', max_length=50, null=True, blank=True)
    local_address2 = models.CharField('상세주소', max_length=25, null=True, blank=True)
    local_address3 = models.CharField('참고항목', max_length=20, null=True, blank=True)
    area_usage = models.CharField('용도지역지구', max_length=50, null=True, blank=True)
    build_size = models.CharField('건축규모', max_length=50, null=True, blank=True)
    num_unit = models.PositiveSmallIntegerField('세대(호/실)수', null=True, blank=True)
    buy_land_extent = models.DecimalField('대지매입면적', max_digits=12, decimal_places=4, null=True, blank=True)
    scheme_land_extent = models.DecimalField('계획대지면적', max_digits=12, decimal_places=4, null=True, blank=True)
    donation_land_extent = models.DecimalField('기부채납면적', max_digits=11, decimal_places=4, null=True, blank=True)
    on_floor_area = models.DecimalField('지상연면적', max_digits=12, decimal_places=4, null=True, blank=True)
    under_floor_area = models.DecimalField('지하연면적', max_digits=11, decimal_places=4, null=True, blank=True)
    total_floor_area = models.DecimalField('총 연면적', max_digits=12, decimal_places=4, null=True, blank=True)
    build_area = models.DecimalField('건축면적', max_digits=11, decimal_places=4, null=True, blank=True)
    floor_area_ratio = models.DecimalField('용적율', max_digits=7, decimal_places=4, null=True, blank=True)
    build_to_land_ratio = models.DecimalField('건폐율', max_digits=6, decimal_places=4, null=True, blank=True)
    num_legal_parking = models.PositiveSmallIntegerField('법정주차대수', null=True, blank=True)
    num_planed_parking = models.PositiveSmallIntegerField('계획주차대수', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', '-start_year', 'id']
        verbose_name = '01. 프로젝트'
        verbose_name_plural = '01. 프로젝트'


class UnitType(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='프로젝트', related_name='types')
    name = models.CharField('타입명칭', max_length=10)
    color = models.CharField('타입색상', max_length=7)
    average_price = models.PositiveIntegerField('평균가격')
    num_unit = models.PositiveSmallIntegerField('세대수')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = '02. 타입 정보'
        verbose_name_plural = '02. 타입 정보'


class UnitFloorType(models.Model):  # 층별 타입
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='프로젝트', related_name='floors')
    start_floor = models.PositiveIntegerField('시작 층')
    end_floor = models.PositiveIntegerField('종료 층')
    alias_name = models.CharField('층별 범위 명칭', max_length=50)

    def __str__(self):
        return self.alias_name

    class Meta:
        ordering = ['-project', '-end_floor', 'id']
        verbose_name = '03. 층별 조건'
        verbose_name_plural = '03. 층별 조건'


class ContractUnit(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='프로젝트', related_name='units')
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE, verbose_name='타입')
    unit_code = models.CharField('코드번호', max_length=8)
    contract = models.OneToOneField('contract.Contract', on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='계약')

    def __str__(self):
        return f'{self.unit_code}'

    class Meta:
        ordering = ['unit_code', '-project']
        verbose_name = '04. 계약 유닛'
        verbose_name_plural = '04. 계약 유닛'


class UnitNumber(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.PROTECT, verbose_name='프로젝트')
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE, verbose_name='타입')
    floor_type = models.ForeignKey('UnitFloorType', on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name='층범위 타입')
    bldg_no = models.CharField('동', max_length=5, blank=True)
    bldg_unit_no = models.CharField('호수', max_length=5, blank=True)
    contract_unit = models.OneToOneField(ContractUnit, on_delete=models.SET_NULL, null=True, blank=True,
                                         verbose_name='계약유닛')
    bldg_line = models.PositiveSmallIntegerField('라인')
    floor_no = models.PositiveSmallIntegerField('층수')
    is_hold = models.BooleanField('홀딩 여부', default=False)
    hold_reason = models.CharField('홀딩 사유', max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.bldg_no}-{self.bldg_unit_no}'

    class Meta:
        ordering = ['bldg_no', '-project']
        verbose_name = '05. 동별 호수'
        verbose_name_plural = '05. 동별 호수'


class ProjectBudget(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.PROTECT, verbose_name='프로젝트')
    account_d1 = models.ForeignKey('rebs.ProjectAccountD1', on_delete=models.PROTECT, verbose_name='예산항목1')
    account_d2 = models.ForeignKey('rebs.ProjectAccountD2', on_delete=models.PROTECT, verbose_name='예산항목2')
    budget = models.PositiveBigIntegerField(verbose_name='예산금액')

    class Meta:
        ordering = ('account_d2', '-project')
        verbose_name = '06. 프로젝트 예산'
        verbose_name_plural = '06. 프로젝트 예산'


class Site(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.PROTECT, verbose_name='프로젝트')
    order = models.PositiveSmallIntegerField('순서')
    district = models.CharField('행정동', max_length=10)
    lot_number = models.CharField('지번', max_length=10)
    site_purpose = models.CharField('지목', max_length=10)
    official_area = models.DecimalField('대지면적', max_digits=10, decimal_places=4)
    returned_area = models.DecimalField('환지면적', max_digits=10, decimal_places=4, null=True, blank=True)
    rights_restrictions = models.TextField('권리제한사항', null=True, blank=True)
    dup_issue_date = models.DateField('등본발급일', null=True, blank=True)
    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    def __str__(self):
        return f'{self.district} {self.lot_number}'

    class Meta:
        ordering = ('order', 'lot_number', '-project')
        verbose_name = '07. 사업부지 목록'
        verbose_name_plural = '07. 사업부지 목록'


class SiteOwner(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.PROTECT, verbose_name='프로젝트')
    owner = models.CharField('소유자', max_length=10)
    date_of_birth = models.DateField('생년월일', null=True, blank=True)
    phone1 = models.CharField('주연락처', max_length=13, null=True, blank=True)
    phone2 = models.CharField('비상연락처', max_length=13, null=True, blank=True)
    zipcode = models.CharField('우편번호', max_length=5, null=True, blank=True)
    address1 = models.CharField('주소', max_length=50, null=True, blank=True)
    address2 = models.CharField('상세주소', max_length=25, null=True, blank=True)
    address3 = models.CharField('참고항목', max_length=25, null=True, blank=True)
    OWN_CHOICES = (('1', '개인'), ('2', '법인'), ('3', '국공유지'))
    own_sort = models.CharField('소유구분', max_length=1, choices=OWN_CHOICES)
    sites = models.ManyToManyField(Site, through='SiteOwnshipRelationship', through_fields=('site_owner', 'site'),
                                   verbose_name='소유부지')
    counsel_record = models.TextField('상담기록', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='등록자')
    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    def __str__(self):
        return self.owner

    class Meta:
        ordering = ('-id',)
        verbose_name = '08. 사업부지 소유자'
        verbose_name_plural = '08. 사업부지 소유자'


class SiteOwnshipRelationship(models.Model):
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    site_owner = models.ForeignKey(SiteOwner, on_delete=models.SET_NULL, null=True)
    ownership_ratio = models.DecimalField('소유지분', max_digits=10, decimal_places=7, null=True, blank=True)
    owned_area = models.DecimalField('소유면적', max_digits=10, decimal_places=4, null=True, blank=True)
    acquisition_date = models.DateField('소유권 취득일', null=True, blank=True)

    def __str__(self):
        return f'{self.site} {self.site_owner}'

    class Meta:
        ordering = ('id',)
        verbose_name = '09. 사업부지 소유관계'
        verbose_name_plural = '09. 사업부지 소유관계'


class SiteContract(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.PROTECT, verbose_name='프로젝트')
    owner = models.ForeignKey(SiteOwner, on_delete=models.CASCADE, verbose_name='소유자')
    contract_date = models.DateField('계약체결일')
    total_price = models.PositiveBigIntegerField('총매매대금')
    down_pay1 = models.PositiveBigIntegerField('계약금1', null=True, blank=True)
    down_pay1_is_paid = models.BooleanField('계약금1 지급여부', default=False)
    down_pay2 = models.PositiveBigIntegerField('계약금2', null=True, blank=True)
    down_pay2_date = models.DateField('계약금2 지급일', null=True, blank=True)
    down_pay2_is_paid = models.BooleanField('계약금2 지급여부', default=False)
    inter_pay1 = models.PositiveBigIntegerField('중도금1', null=True, blank=True)
    inter_pay1_date = models.DateField('중도금1 지급일', null=True, blank=True)
    inter_pay1_is_paid = models.BooleanField('중도금1 지급여부', default=False)
    inter_pay2 = models.PositiveBigIntegerField('중도금2', null=True, blank=True)
    inter_pay2_date = models.DateField('중도금2 지급일', null=True, blank=True)
    inter_pay2_is_paid = models.BooleanField('중도금2 지급여부', default=False)
    remain_pay = models.PositiveBigIntegerField('잔금')
    remain_pay_date = models.DateField('잔금 지급일', null=True, blank=True)
    remain_pay_is_paid = models.BooleanField('잔금 지급여부', default=False)
    ownership_completion = models.BooleanField('소유권 확보여부', default=False)
    acc_bank = models.CharField('은행', max_length=20)
    acc_number = models.CharField('계좌번호', max_length=20)
    acc_owner = models.CharField('예금주', max_length=20)
    note = models.TextField('특이사항', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='등록자')
    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    def __str__(self):
        return f'{self.owner.owner} - [{self.total_price}]'

    class Meta:
        ordering = ('-id',)
        verbose_name = '10. 사업부지 계약현황'
        verbose_name_plural = '10. 사업부지 계약현황'
