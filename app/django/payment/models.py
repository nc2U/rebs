from django.db import models


class SalesPriceByGT(models.Model):  # 차수별 타입별 분양가격
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, verbose_name='프로젝트')
    order_group = models.ForeignKey('contract.OrderGroup', on_delete=models.CASCADE, verbose_name='차수')
    unit_type = models.ForeignKey('items.UnitType', on_delete=models.CASCADE, verbose_name='타입')
    unit_floor_type = models.ForeignKey('items.UnitFloorType', on_delete=models.PROTECT, verbose_name='층별타입')
    price_build = models.PositiveIntegerField('건물가', null=True, blank=True)
    price_land = models.PositiveIntegerField('대지가', null=True, blank=True)
    price_tax = models.PositiveIntegerField('부가세', null=True, blank=True)
    price = models.PositiveIntegerField('분양가격')

    def __str__(self):
        return f'{self.price}'

    class Meta:
        ordering = ('order_group', 'unit_type', 'unit_floor_type', 'project')
        verbose_name = '01. 프로젝트 분양가 관리'
        verbose_name_plural = '01. 프로젝트 분양가 관리'


class InstallmentPaymentOrder(models.Model):  # 분할 납부 차수 등록
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, verbose_name='프로젝트')
    SORT_CHOICES = (('1', '계약금'), ('2', '중도금'), ('3', '잔금'))
    pay_sort = models.CharField('종류', max_length=1, choices=SORT_CHOICES, default='1')
    pay_code = models.PositiveSmallIntegerField('납입회차 코드', help_text='프로젝트 내에서 모든 납부회차를 고유 순서대로 숫자로 부여한다.')
    pay_time = models.PositiveSmallIntegerField('납부순서',
                                                help_text='''동일 납부회차에 2가지 항목을 별도로 납부하여야 하는 경우(ex: 분담금 + 업무대행료)
                                                하나의 납입회차 코드(ex: 1)에 2개의 납부순서(ex: 1, 2)를 등록한다.''')
    pay_ratio = models.DecimalField('회당 납부비율(%)', default=10, max_digits=7, decimal_places=4,
                                    help_text='분양가 대비 납부비율, 계약금 항목인 경우 Downpamy 테이블 데이터 우선, 잔금 항목인 경우 분양가와 비교 차액 데이터 우선')
    pay_name = models.CharField('납부회차 명', max_length=20)
    alias_name = models.CharField('회차 별칭', max_length=20, blank=True)
    is_pm_cost = models.BooleanField('PM용역비 여부', default=False)
    pay_due_date = models.DateField('납부기한일', null=True, blank=True)
    extra_due_date = models.DateField('납부유예일', null=True, blank=True,
                                      help_text='연체료 계산 기준은 납부기한일이 원칙이나 이 값이 있는 경우 납부유예일을 연체료 계산 기준으로 한다.')

    def __str__(self):
        return f'[{self.get_pay_sort_display()}] - {self.pay_name}'

    class Meta:
        ordering = ['-project', 'pay_code']
        verbose_name = '02. 납입회차 관리'
        verbose_name_plural = '02. 납입회차 관리'


class DownPayment(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, verbose_name='프로젝트')
    order_group = models.ForeignKey('contract.OrderGroup', on_delete=models.CASCADE, verbose_name='차수정보')
    unit_type = models.ForeignKey('items.UnitType', on_delete=models.CASCADE, verbose_name='타입정보')
    payment_amount = models.PositiveIntegerField('회별 납부금액')

    def __str__(self):
        return f'{self.payment_amount}'

    class Meta:
        ordering = ('id',)
        verbose_name = '03. 타입별 계약금 관리'
        verbose_name_plural = '03. 타입별 계약금 관리'


class OverDueRule(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, verbose_name='프로젝트')
    term_start = models.IntegerField('최소연체일', null=True, blank=True, help_text='비어있을 경우 최대 음수')
    term_end = models.IntegerField('최대연체일', null=True, blank=True, help_text='비어있을 경우 최대 양수')
    rate_year = models.DecimalField('연체이율', max_digits=4, decimal_places=2)

    def __str__(self):
        ts = str(self.term_start) + '일' if self.term_start != None else 'Min'
        te = str(self.term_end) + '일' if self.term_end != None else 'Max'
        return f'{ts} - {te}'

    class Meta:
        ordering = ('-id',)
        verbose_name = '04. 선납할인/연체이율 관리'
        verbose_name_plural = '04. 선납할인/연체이율 관리'
