import math
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# --------------------------------------------------------
from datetime import date, timedelta
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from django.db.models import Sum
from contract.models import Contract
from notice.models import SalesBillIssue
from cash.models import (SalesPriceByGT, ProjectCashBook,
                         InstallmentPaymentOrder, DownPayment)

TODAY = date.today()


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'rebs/main/1_1_dashboard.html'


def memu2_1(request):
    return render(request, 'rebs/main/2_1_schedule.html')


class PdfExportBill(View):
    """고지서 리스트"""

    def get(self, request):
        project = request.GET.get('project')  # 프로젝트 ID

        context = {}  # 전체 데이터 딕셔너리
        context['data_list'] = []  # 계약 건별 데이터 리스트
        context['issue_date'] = request.GET.get('date')  # 고지서 발행일
        context['bill_info'] = SalesBillIssue.objects.get(project_id=project)  # 고지서 일반 정보
        inspay_order = InstallmentPaymentOrder.objects.filter(project_id=project)  # 전체 납부회차 리스트
        now_due_order = context['bill_info'].now_payment_order.pay_code \
            if context['bill_info'].now_payment_order else 2  # 당회 납부 회차

        contractor_list = request.GET.get('seq').split('-')  # 계약 건 ID 리스트

        # 해당 계약건에 대한 데이터 정리 --------------------------------------- start
        for cont_id in contractor_list:  # 선택된 계약 건 수만큼 반복

            bill_data = self.get_bill_data(project, cont_id, inspay_order, now_due_order)
            context['data_list'].append(bill_data)

        # 해당 계약건에 대한 데이터 정리 --------------------------------------- end

        html_string = render_to_string('pdf/bill_control.html', context)
        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/mypdf.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="payment_bill({len(contractor_list)}).pdf"'
            return response

    def get_bill_data(self, project, cont_id, inspay_order, now_due_order):
        """
        param =>
        :project: project
        :cont_id: cont_id
        :inspay_order:
        :now_due_order:

        return =>
        """
        bill_data = {}  # 현재 계약 정보 딕셔너리

        # 계약 건 객체
        bill_data['contract'] = contract = self.get_contract(cont_id)

        try:
            unit = contract.keyunit.houseunit
        except:
            unit = None

        # 동호수
        bill_data['unit'] = unit

        # 이 계약 건 분양가 (계약금, 중도금, 잔금 약정액)
        this_price, down, medium, balance = self.get_this_price(project, contract, unit, inspay_order)
        bill_data['price'] = this_price if unit else '동호 지정 후 고지'  # 이 건 분양가격

        # 납부목록, 완납금액 구하기 ------------------------------------------
        paid_list, paid_sum_total = self.get_paid(contract)
        # --------------------------------------------------------------

        # 해당 계약 건의 회차별(계약금 중도금 잔금) 약정액 리스트 구하기
        amount = {'1': down, '2': medium, '3': balance}
        pay_amounts_all = [amount[pa.pay_sort] for pa in inspay_order]  # 회차별 약정액 리스트

        # 해당 계약 건의 회차별 관련 정보
        orders_info = self.get_orders_info(inspay_order, pay_amounts_all, paid_sum_total)
        # 완납 회차
        paid_code = self.get_paid_code(orders_info, paid_sum_total)

        # ■ 계약 내용 -----------------------------------------------------
        bill_data['cont_content'] = self.get_cont_content(contract, this_price, unit)

        # ■ 당회 납부대금 안내 ----------------------------------------------
        bill_data['this_pay_info'] = self.get_this_pay_info(cont_id,
                                                            orders_info,
                                                            inspay_order,
                                                            now_due_order,
                                                            paid_code)

        # 당회 납부대금 합계
        bill_data['this_pay_sum'] = {
            'amount_sum': sum([pi["amount"] for pi in bill_data['this_pay_info']]),
            'unpaid_sum': sum([pi["unpaid"] for pi in bill_data['this_pay_info']]),
            'penalty_sum': sum([pi["penalty"] for pi in bill_data['this_pay_info']]),
            'amount_total': sum([pi["sum_amount"] for pi in bill_data['this_pay_info']]),
        }

        # ■ 계좌번호 안내 ------------------------------------------------
        bill_data['bank_accounts'] = (bill_data['this_pay_sum']['amount_total'],
                                      sum([pm['pm_cost_sum'] for pm in orders_info]))

        # ■ 납부약정 및 납입내역 -------------------------------------------
        bill_data['paid_orders1'] = self.get_paid_orders(cont_id, orders_info, inspay_order, now_due_order)

        bill_data['remain_orders'] = self.get_remain_orders()

        bill_data['pay_amount_sum'] = self.get_pay_amount_sum()
        # --------------------------------------------------------------

        pay_amount_total = 0  # 납부 지정회차까지 약정금액 합계

        pay_amount_paid = 0  # 완납 회차까지 약정액 합계
        paid_pay_code = 0  # 완납회차
        pm_cost_sum = 0  # pm 용역비 누계
        apply_pay = 0  # 가산금 적용액

        payment_list = []  # 회차별 납부금액
        paid_date_list = []  # 회차별 최종 수납일자
        due_date_list = []  # 회차별 납부기한

        def_pay_list = []  # 회차별 지연금액 리스트
        delay_day_list = []  # 회차별 지연일수
        late_fee_list = []  # 연체료 리스트
        past_late_fee_list = []
        current_late_fee_list = []

        first_paid_date = None  # 최초 계약금 완납일

        # --------------------------------------------------------------
        for i, ipo in enumerate(inspay_order):  # 납부회차 전체 순회
            pay_amount = pay_amounts_all[i]  # 약정금액

            pay_amount_total += pay_amount  # 약정금액 누계

            if paid_sum_total >= pay_amount_total:  # 기 납부총액이 약정액보다 같거나 큰지 검사
                paid_pay_code = ipo.pay_code  # 완납회차 추출
                pay_amount_paid += pay_amount  # 완납회차까지 약정액 누계

            if ipo.is_pm_cost:
                pm_cost_sum += pay_amount  # pm 용역비 누계

            # 회차별 납부 해야할 금액 ----------------------------------------------------------
            now_payment = paid_list.filter(installment_order=ipo)  # 현재 회차 납부 데이터
            paid_date = now_payment.latest('deal_date').deal_date if now_payment else None  # 현재회차 최종 납부일
            now_paied_sum = now_payment.aggregate(Sum('income'))['income__sum']  # 현재 회차 납부액 합계
            paid_amount = now_paied_sum if now_paied_sum else 0

            if ipo.pay_code == 1:
                first_paid_date = paid_date  # 계약금 납부일
            payment_list.append(paid_amount)  # 회차별 납부금액
            paid_date_list.append(paid_date)  # 회차별 최종 수납일자

            # 계약일과 최초 계약금 납부일 중 늦은 날을 기점으로 30일
            reference_date = first_paid_date if first_paid_date and (
                    first_paid_date > contract.contractor.contract_date) else contract.contractor.contract_date

            if ipo.pay_time == 1 or ipo.pay_code == 1:  # 최초 계약금일 때
                due_date = contract.contractor.contract_date  # 납부기한일

            elif ipo.pay_time == 2 or ipo.pay_code == 2:  # 2차 계약금일 때
                due_date = reference_date + timedelta(days=30)  # 납부기한 = 기준일 30일 후
                if ipo.pay_due_date:  # 당회차 납부기한이 설정되어 있을 때 -> 계약후 30일 후와 설정일 중 늦은 날을 납부기한으로 한다.
                    due_date = due_date if due_date > ipo.pay_due_date else ipo.pay_due_date  # 납부기한

            else:  # 3회차 이후 납부회차인 경우
                if ipo.pay_due_date:
                    due_date = ipo.pay_due_date if ipo.pay_due_date > reference_date + timedelta(
                        days=30) else reference_date + timedelta(days=30)  # 납부기한
                else:
                    due_date = None

            # extra_date 이전의 연체일수를 계산하지 않는다. 즉 extra_date 이후의 연체 발생 건부터 적용한다.
            extra_date = ipo.extra_due_date if ipo.extra_due_date else due_date  # 납부유예일
            if not ipo.pay_due_date or extra_date > due_date:  # 납부유예일이 있고 납부기한일보다 늦으면
                due_date = extra_date  # extra_date 가 설정되어 있고 납부기한보다 늦으면 extra_date를 납부기한으로 한다.

            due_date_list.append(due_date)  # 회차별 납부일자

            # 지연일수 및 가산금 구하기
            unpaid = pay_amount - paid_amount  # 지연금 = 약정 금액 - 납부한 금액
            def_pay_list.append(unpaid)  # 지연금 리스트

            delay_paid_sum = 0  # 지연금 총 납부액
            delay_paid_date = date.today()  # 지연 기준일

            early_days = 0

            if unpaid >= 0:
                delay_paid = paid_list.filter(installment_order__gt=ipo)
                for dp in delay_paid:
                    delay_paid_sum += dp.income
                    if delay_paid_sum > unpaid:
                        delay_paid_date = dp.deal_date  # 지연금 완납일자
                        break
            else:  # 약정금 초과 납부(선납) 시
                next_order = inspay_order.filter(pay_code__gt=ipo.pay_code).first()
                if next_order.pay_due_date:
                    early = next_order.pay_due_date - paid_date
                    early_days = early.days if early.days > 0 else 0

            if extra_date and extra_date > delay_paid_date:  # 납부유예일 > 오늘 또는 완납일자
                delay_days = 0  # 지연일수
            else:
                delay = 0  # delay_paid_date - extra_date  # 미수 완납일 - 미수 발생일
                delay_days = 0  # delay.days  # 지연일수

            apply_pay += unpaid
            late_fee_list.append(self.get_late_fee(apply_pay, delay_days, early_days))
            if ipo.pay_code <= paid_pay_code + 1:
                past_late_fee_list.append(self.get_late_fee(apply_pay, delay_days, early_days))
            else:
                current_late_fee_list.append(self.get_late_fee(apply_pay, delay_days, early_days))

            if unpaid >= 0:
                delay_day_list.append(delay_days)  # 회차별 지연일수
            else:
                delay_day_list.append(early_days)  # 회차별 선납일수

            if ipo.pay_code == now_due_order:  # 순회 회차가 지정회차와 같으면 순회중단
                break
        # --------------------------------------------------------------

        # ■ 당회 납부대금 안내----------------------------------------------
        unpaid_orders_all = inspay_order.filter(pay_code__gt=paid_pay_code)  # 최종 기납부회차 이후 납부회차
        bill_data['unpaid_orders'] = unpaid_orders = unpaid_orders_all.filter(
            pay_code__lte=now_due_order)  # 최종 기납부회차 이후부터 납부지정회차 까지 회차그룹

        bill_data['second_date'] = contract.contractor.contract_date + timedelta(days=30)  # 2회차 납부일 (계약후 30일)
        bill_data['pay_amount'] = 0
        bill_data['pay_amount_sum'] = 0
        summary_late_fee_list = []
        for i, uo in enumerate(unpaid_orders):
            if uo.pay_sort == '1':
                bill_data['pay_amount'] = down
            elif uo.pay_sort == '2':
                bill_data['pay_amount'] = medium
            else:
                bill_data['pay_amount'] = balance
            bill_data['pay_amount_sum'] += bill_data['pay_amount']
            if i == 0:
                summary_late_fee_list.append(sum(past_late_fee_list))
            else:
                summary_late_fee_list.append(current_late_fee_list[i - 1])
        bill_data['cal_unpaid'] = pay_amount_paid - paid_sum_total
        bill_data['cal_unpaid_sum'] = pay_amount_total - paid_sum_total  # 미납액 = 약정액 - 납부액
        bill_data['summary_late_fee_list'] = list(reversed(summary_late_fee_list))
        bill_data['summary_late_fee_sum'] = sum(summary_late_fee_list)
        # --------------------------------------------------------------

        # ■ 계좌번호 안내--------------------------------------------------
        bill_data['pay_amount_total'] = pay_amount_total
        bill_data['pm_cost_sum'] = pm_cost_sum
        # --------------------------------------------------------------

        # ■ 납부약정 및 납입내역--------------------------------------------
        bill_data['paid_orders'] = inspay_order.filter(pay_code__lte=now_due_order)  # 지정회차까지 회차
        bill_data['due_date_list'] = list(reversed(due_date_list))  # 회차별 납부일자
        for po in bill_data['paid_orders']:
            if po.pay_sort == '1':
                bill_data['pay_amount'] = down
            elif po.pay_sort == '2':
                bill_data['pay_amount'] = medium
            else:
                bill_data['pay_amount'] = balance
        bill_data['paid_date_list'] = list(reversed(paid_date_list))  # 회차별 최종 수납일자
        bill_data['payment_list'] = list(reversed(payment_list))  # 회차별 납부금액
        bill_data['def_pay_list'] = list(reversed(def_pay_list))  # 회차별 지연금 리스트
        bill_data['delay_day_list'] = list(reversed(delay_day_list))  # 회차별 지연일수
        bill_data['late_fee_list'] = list(reversed(late_fee_list))  # 연체료 리스트

        # 잔여 약정 목록
        bill_data['remaining_orders'] = remaining_orders = inspay_order.filter(pay_code__gt=now_due_order)
        if not bill_data['unit']:
            bill_data['remaining_orders'] = remaining_orders.filter(pay_sort='1')

        num = unpaid_orders.count() + 1 if pm_cost_sum else unpaid_orders.count()
        rem_blank = 0 if bill_data['unit'] else remaining_orders.count()
        blank_line = (15 - (num + inspay_order.count())) + rem_blank
        bill_data['blank_line'] = '.' * blank_line

        bill_data['paid_sum'] = paid_sum_total  # 납부액 합계
        bill_data['def_pay_sum'] = sum(def_pay_list)  # 미납금 합계
        bill_data['delay_day_sum'] = sum(delay_day_list)
        bill_data['late_fee_sum'] = sum(late_fee_list)  # 연체료 합계
        # --------------------------------------------------------------
        return bill_data

    def get_contract(self, id):
        """ ■ 계약 가져오기
        :param id: 계약자 아이디
        :return object(contract):
        """
        return Contract.objects.get(contractor__id=id)

    def get_this_price(self, project, contract, unit, inspay_order):
        """ ■ 해당 계약 건 분양가 구하기
        :param project: 프로젝트 정보
        :param contract: 계약 정보
        :param unit: 동호수 정보
        :param inspay_order: 전체 회차 정보
        :return int(this_price), int(down), int(medium), int(balance):
        """
        # 총 공급가액(분양가) 구하기
        group = contract.order_group  # 차수
        type = contract.unit_type  # 타입

        # 해당 계약건 분양가 # this_price = '동호 지정 후 고지'
        this_price = contract.keyunit.unit_type.average_price

        prices = SalesPriceByGT.objects.filter(project_id=project, order_group=group, unit_type=type)

        if unit:
            floor = contract.keyunit.houseunit.floor_type
            this_price = prices.get(unit_floor_type=floor).price

        # 계약금 구하기 ----------------------------------------------------------------
        down_num = inspay_order.filter(pay_sort='1').count()
        try:
            dp = DownPayment.objects.get(
                project_id=project,
                order_group=contract.order_group,
                unit_type=contract.keyunit.unit_type
            )
            down = dp.payment_amount
        except:
            pn = round(down_num / 2)
            down = int(this_price * 0.1 / pn)
        down_total = down * down_num
        # ---------------------------------------------------------------------------

        # 중도금 구하기 ----------------------------------------------------------------
        med_num = inspay_order.filter(pay_sort='2').count()
        medium = int(this_price * 0.1)
        medium_total = medium * med_num
        # ---------------------------------------------------------------------------

        # 잔금 구하기 -----------------------------------------------------------------
        bal_num = inspay_order.filter(pay_sort='3').count()
        balance = int((this_price - down_total - medium_total) / bal_num)
        # ---------------------------------------------------------------------------

        return this_price, down, medium, balance

    def get_paid(self, contract):
        """
        :: ■ 기 납부금액 구하기
        :param contract: 계약정보
        :return list(paid_list), int(paid_sum_total):
        """
        paid_list = ProjectCashBook.objects.filter(
            is_contract_payment=True,
            contract=contract,
            income__isnull=False
        ).order_by('installment_order', 'deal_date')  # 해당 계약 건 납부 데이터

        paid_sum_total = paid_list.aggregate(Sum('income'))['income__sum']  # 완납 총금액
        return paid_list, paid_sum_total

    def get_cont_content(self, contract, price, unit):
        """
        :: ■ 계약 내용
        :param contract: 계약정보
        :param unit: 동호수 정보
        :return dict(계약자명, 계약일, 계약번호, 평형, 총 공급가격):
        """
        contractor = contract.contractor.name
        cont_date = contract.contractor.contract_date
        cont_no = contract.keyunit.houseunit if unit else contract.serial_number
        cont_type = contract.keyunit.unit_type
        return {
            'contractor': contractor,
            'cont_date': cont_date,
            'cont_no': cont_no,
            'cont_type': cont_type,
        }

    def get_paid_code(self, orders_info, paid_sum_total):
        return [c['order'].pay_code for c in orders_info if paid_sum_total >= c['sum_pay_amount']][-1]

    def get_this_pay_info(self, cont_id, orders_info, inspay_order, now_due_order, paid_code):
        """
        :: ■ 당회 납부대금 안내
        :param cont_id: 계약자 아이디
        :param orders_info: 회차별 부가정보
        :param inspay_order: 회차 정보
        :param now_due_order: 당회 납부 회차
        :param paid_code: 완납 회차
        :return list(dict(납부회차, 납부 기한, 약정금액, 미납금액, 연체가산금, 납부금액)):
        """
        payment_list = []
        unpaid_orders = inspay_order.filter(pay_code__gt=paid_code,
                                            pay_code__lte=now_due_order)  # 최종 기납부회차 이후부터 납부지정회차 까지 회차그룹
        for order in unpaid_orders:
            cont_ord = list(filter(lambda o: o['order'] == order, orders_info))[0]

            amount = cont_ord['pay_amount']
            unpaid = cont_ord['unpaid_amount']
            penalty = 0

            payment_dict = {
                'order': order,
                'due_date': self.get_due_date(cont_id, order),
                'amount': amount,
                'unpaid': unpaid,
                'penalty': penalty,
                'sum_amount': unpaid + penalty
            }
            payment_list.append(payment_dict)

        return payment_list

    def get_paid_orders(self, cont_id, orders_info, inspay_order, now_due_order):
        """
        :: ■ 납부약정 및 납입내역 - 납입내역
        :param orders_info:
        :param inspay_order:
        :param now_due_order:
        :param paid_sum_total:
        :return list(paid_list):
        """
        paid_list = []
        paid_orders = inspay_order.filter(pay_code__lte=now_due_order)

        for order in paid_orders:
            cont_ord = list(filter(lambda o: o['order'] == order, orders_info))[0]
            amount = cont_ord['pay_amount']

            paid_dict = {
                'order': order.pay_name,
                'due_date': self.get_due_date(cont_id, order),
                'amount': amount,
                'paid_date': '',
                'paid_amt': 0,
                'delayed_amt': 0,
                'penalty_days': 0,
                'panalty_amt': 0,
            }
            paid_list.append(paid_dict)

        return paid_list

    def get_remain_orders(self):
        """
        :: ■ 납부약정 및 납입내역 - 잔여회차
        :param inspay_order:
        :return :
        """
        return 2

    def get_pay_amount_sum(self):
        """
        :: ■ 납부약정 및 납입내역 - 합계 테이블
        :param inspay_order:
        :return :
        """
        return 3

    def get_orders_info(self, inspay_order, pay_amounts_all, paid_sum_total):
        """
        :: 회차별 부가정보
        :param inspay_order: 회차 정보
        :param pay_amounts_all: 전체 약정액 리스트
        :param paid_sum_total: 기 납부 총액
        :return list(dict(order_info_list)): 회차별 부가정보 딕셔너리 리스트
        """
        order_info_list = []
        sum_pay_amount = 0  # 회당 납부 약정액 누계
        pm_cost_sum = 0  # PM 용역비 합계

        for i, order in enumerate(inspay_order):
            info = {}
            info['order'] = order  # 회차
            pay_amount = pay_amounts_all[i]  # 회당 납부 약정액
            info['pay_amount'] = pay_amount  # 회당 납부 약정액
            sum_pay_amount += pay_amount  # 회당 납부 약정액 누계
            info['sum_pay_amount'] = sum_pay_amount  # 회당 납부 약정액 누계
            unpaid = sum_pay_amount - paid_sum_total  # 약정액 누계 - 총 납부액
            info['unpaid_amount'] = unpaid if unpaid < pay_amount else pay_amount  # 미납액
            pm_cost_sum += pay_amount if order.is_pm_cost else 0  # PM 용역비 합계
            info['pm_cost_sum'] = pm_cost_sum  # PM 용역비 합계

            order_info_list.append(info)

        return order_info_list

    def get_due_date(self, cont_id, order):
        """
        :: 납부일자 구하기
        :param cont_id: 계약자 아이디
        :param order: 납부회차
        :return str(due_date): 납부일자
        """
        ref_date = self.get_contract(cont_id).contractor.contract_date

        due_date = ref_date
        due_date = ref_date if order.pay_time == 1 else due_date
        due_date = ref_date + timedelta(days=30) if order.pay_time == 2 else due_date

        due_date = order.pay_due_date if order.pay_due_date else due_date

        due_date = order.extra_due_date if order.extra_due_date else order.pay_due_date
        return due_date

    def get_late_fee(self, amount, delay, early):
        """
        :: 회차별 지연 가산금 계산 함수
        :param amount:
        :param delay:
        :param early:
        :return:
        """
        if amount < 0:
            late_fee = amount * 0.04 * early / 365
        else:
            if delay < 30:
                late_fee = amount * 0.08 * delay / 365
            elif delay < 90:
                late_fee = (amount * 0.08 * 29 / 365) + (amount * 0.1 * (delay - 29) / 365)
            elif delay < 180:
                late_fee = (amount * 0.08 * 29 / 365) + (amount * 0.1 * 60 / 365) + (amount * 0.11 * (delay - 89) / 365)
            else:
                late_fee = (amount * 0.08 * 29 / 365) + (amount * 0.1 * 60 / 365) + (amount * 0.11 * 90 / 365) + (
                        amount * 0.12 * (delay - 179) / 365)

        return math.floor(late_fee / 1000) * 1000


class PdfExportPayments(View):

    def get(self, request):
        context = {}
        project = request.GET.get('project')
        get_contract = request.GET.get('contract')
        context['contract'] = contract = Contract.objects.get(pk=get_contract)
        cont_date = contract.contractor.contract_date
        context['second_pay'] = second_pay = cont_date + timedelta(days=30) if contract else None
        context['ip_orders'] = ip_orders = InstallmentPaymentOrder.objects.filter(project=project)
        context['payments'] = ProjectCashBook.objects.filter(project=project, contract=contract)

        # 1. 분양가격 (차수/타입별/동호수별) 및 계약금, 중도금, 잔금 구하기
        group = contract.order_group  # 차수
        type = contract.keyunit.unit_type  # 타입
        prices = SalesPriceByGT.objects.filter(project_id=project, order_group=group, unit_type=type)  # 그룹 및 타입별 가격대
        this_price = int(round(contract.keyunit.unit_type.average_price, -4))

        try:  # 동호수
            unit = contract.keyunit.houseunit
        except Exception:
            unit = None

        if unit:
            floor = contract.keyunit.houseunit.floor_type
            this_price = prices.get(unit_floor_type=floor).price

        context['unit'] = unit
        context['this_price'] = this_price
        # --------------------------------------------------------------

        # 2. 실입금액
        paid_list = ProjectCashBook.objects.filter(contract=contract)
        context['now_payments'] = paid_list.aggregate(Sum('income'))['income__sum']  # 기 납부총액

        # 3. 납부원금 (현재 지정회차 + 납부해야할 금액 합계)
        ## 계약금 구하기
        inspay_order = InstallmentPaymentOrder.objects.filter(project=project)  # 해당 건 전체 약정 회차
        down_num = inspay_order.filter(pay_sort='1').count()
        try:
            dp = DownPayment.objects.get(project_id=project, order_group=contract.order_group,
                                         unit_type=contract.keyunit.unit_type)
            context['down'] = dp.payment_amount
        except:
            pn = round(down_num / 2)
            context['down'] = int(this_price * 0.1 / pn)
        down_total = context['down'] * down_num

        ## 중도금 구하기
        med_num = inspay_order.filter(pay_sort='2').count()
        context['medium'] = int(this_price * 0.1)
        medium_total = context['medium'] * med_num

        ## 잔금 구하기
        bal_num = inspay_order.filter(pay_sort='3').count()
        context['balance'] = int((this_price - down_total - medium_total) / bal_num)

        set_order1 = ip_orders.filter(pay_due_date__lt=TODAY).latest('pay_due_date')
        due_order = SalesBillIssue.objects.get(project_id=project)
        now_due_order = due_order.now_payment_order.pay_code if due_order.now_payment_order else 2
        set_order2 = ip_orders.filter(pay_time__lte=now_due_order).latest('pay_time')
        set_order = set_order1 if set_order1.pay_time >= set_order2.pay_time else set_order2
        due_installment = InstallmentPaymentOrder.objects.filter(pay_time__lte=set_order.pay_time)

        pay_amount_total = 0  # 지정회차까지 약정액 합계

        for di in due_installment:
            if di.pay_sort == '1':
                pay_amount = context['down']
            if di.pay_sort == '2':
                pay_amount = context['medium']
            if di.pay_sort == '3':
                pay_amount = context['balance']
            pay_amount_total += pay_amount  # 지정회차까지 약정액 합계 (+)

        context['due_payments'] = pay_amount_total
        context['paid_orders'] = paid_orders = inspay_order.filter(
            pay_code__lte=now_due_order)  # 지정회차까지 회차
        paid_date_list = []  # 회차별 최종 수납일자
        payments = []  # 회차별 납부금액
        adj_days = []  # 회차별 지연일수

        for po in paid_orders:
            if po.pay_time == 1 or po.pay_code == 1:
                due_date = cont_date
            elif po.pay_time == 2 or po.pay_code == 2:
                if po.pay_due_date:
                    due_date = second_pay if second_pay > po.pay_due_date else po.pay_due_date
                else:
                    due_date = second_pay
            else:
                if po.pay_due_date:
                    due_date = po.pay_due_date if po.pay_due_date > cont_date else cont_date
                else:
                    due_date = None

            pl = paid_list.filter(installment_order=po)
            pld = pl.latest('deal_date').deal_date if pl else None
            paid_date_list.append(pld)  # 회차별 최종 수납일자

            payments.append(pl.aggregate(Sum('income'))['income__sum'])  # 회차별 납부금액

            ad = pl.latest('deal_date').deal_date - due_date if pl else None
            if po.pay_time <= 2:
                add = ad.days if pl and ad.days > 0 else None
            else:
                add = ad.days if pl else None
            adj_days.append(add)  # 회차별 지연일수

        context['paid_date_list'] = list(reversed(paid_date_list))  # 회차별 최종 수납일자
        context['payments'] = list(reversed(payments))  # 회차별 납부금액
        context['adj_days'] = list(reversed(adj_days))  # 회차별 지연일수

        html_string = render_to_string('pdf/payments_by_contractor.html', context)

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/mypdf.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="payments_contractor.pdf"'
            return response

        return response
