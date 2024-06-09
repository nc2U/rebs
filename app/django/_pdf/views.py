from datetime import date, datetime, timedelta
from itertools import accumulate
# --------------------------------------------------------
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from weasyprint import HTML

from cash.models import ProjectCashBook
from contract.models import Contract
from notice.models import SalesBillIssue
from payment.models import InstallmentPaymentOrder, SpecialPaymentOrder, SpecialDownPay

TODAY = date.today()


def get_contract(cont_id):
    """ ■ 계약 가져오기
    :param cont_id: 계약자 아이디
    :return object(contract: 계약 건):
    """
    return Contract.objects.get(pk=cont_id)


def get_paid(contract, simple_orders, is_past=False):
    """
    :: ■ 기 납부금액 구하기
    :param contract: 계약정보
    :param simple_orders: 회차정보
    :param is_past: 변경 약정에 의한 가산금 산출 여부
    :return list(paid_list: 납부 건 리스트), int(paid_sum_total: 납부 총액):
    """
    paid_list = ProjectCashBook.objects.filter(
        income__isnull=False,
        project_account_d3__in=(1, 4),  # 분(부)담금 or 분양수입금
        contract=contract
    ).order_by('deal_date', 'id')  # 해당 계약 건 납부 데이터

    paid_list = paid_list.filter(installment_order__pay_sort='1') if is_past else paid_list

    pay_list = [p.income for p in paid_list]  # 입금액 추출 리스트
    paid_sum_list = list(accumulate(pay_list))  # 입금액 리스트를 시간 순 누계액 리스트로 변경

    ord_list = []
    paid_dict_list = []

    for i, paid in enumerate(paid_list):  # 입금액 리스트를 순회
        curr_total = paid_sum_list[i]  # 회차별 납부액 누계 추출
        # 약정액누계 보다 납부액 누계가 큰(<=)인 회차 별칭 리스트
        paid_ords = [o['name'] for o in list(filter(lambda o: o['amount_total'] <= curr_total, simple_orders))]
        paid_ord_name = paid_ords[len(paid_ords) - 1] if len(paid_ords) > 0 else None  # 당회 완납이면 회차 별칭 추출
        paid_ord_name = paid_ord_name if paid_ord_name not in ord_list else None  # ord_list 요소와 중복이 아니면 완납회차 별칭 추출
        ord_list.append(paid_ord_name)  # 납부회차 별칭 리스트 추가
        diff = [curr_total - o['amount_total'] for o in simple_orders if
                o['amount_total'] <= curr_total]  # 회차별 납부액누계가 약정액누계 보다 크면 그 차액 리스트 생성
        diff = diff[len(diff) - 1] if len(diff) else 0  # 당회 과납 차액 추출
        paid_dict = {'paid': paid, 'sum': curr_total, 'order': paid_ord_name,
                     'diff': diff}  # {'paid': 회별납부액, 'sum': 회별납부액누계, 'order': '당회 완납 시 별칭', 'diff': 당회 과납차액}
        paid_dict_list.append(paid_dict)
    paid_sum_total = paid_list.aggregate(Sum('income'))['income__sum']  # 완납 총금액
    paid_sum_total = paid_sum_total if paid_sum_total else 0

    return paid_dict_list, paid_sum_total


def get_simple_orders(pay_orders, contract, amount):
    """
    :: 약식 납부회차 구하기
    :param pay_orders:
    :param contract:
    :param amount:
    :return: dict 형식 납부회차 리스트
    """
    simple_orders = []

    amount_total = 0
    for order in pay_orders:
        amount_total += amount[order.pay_sort]  # 회차별 약정금 누계
        ord_info = {
            'name': order.alias_name if order.alias_name else order.pay_name,  # 회차별 별칭
            'due_date': get_due_date_per_order(contract, order, pay_orders),  # 회차별 납부기한
            'amount': amount[order.pay_sort],  # 회차별 약정금
            'amount_total': amount_total,  # 회차별 약정금 누계
        }
        simple_orders.append(ord_info)

    return simple_orders


def get_due_amount(pay_orders, contract, amount):
    """
    :: 약정금 누계 계산 함수
    :param pay_orders: 전체 납부회차 쿼리셋
    :param contract: contract 객체
    :param amount: {'1': down, '2': middle, '3': remain}
    :return: int 현재 회차까지 납부 약정액 합계
    """
    total_amounts = 0
    # 약정회차 리스트
    due_orders = get_due_orders(contract, pay_orders)
    for order in due_orders:
        total_amounts += amount[order.pay_sort]
    return total_amounts


def is_due(due_date):
    """
    :: 주어진 날짜가 기도래 납부기한에 해당하는지 여부
    :param due_date:
    :return: bool -> 기도래 기한 여부
    """
    return due_date and due_date <= TODAY


def get_due_date_per_order(contract, order, pay_orders):
    """
    :: 회차 별 납부 일자 구하기
    :param contract: 계약자 객체
    :param order: 납부 회차 객체
    :return str(due_date): 회차 별 약정 납부 일자
    """

    due_date = contract.contractor.contract_date  # 계약일 (default 납부기한 = 계약일)

    if order.pay_code >= 2:
        elapsed_days = pay_orders.filter(pay_code__lte=order.pay_code) \
            .aggregate(elapsed_days=Sum('days_since_prev'))['elapsed_days']
        due_date = due_date + timedelta(days=elapsed_days) if elapsed_days else due_date

        pd_date = order.pay_due_date
        ed_date = order.extra_due_date

        if pd_date and pd_date > due_date:
            due_date = pd_date
        if ed_date and ed_date > due_date:
            due_date = ed_date
    return due_date


def get_due_orders(contract, pay_orders):
    """
    :: 기도래 납부 회차 객체 리스트 구하기
    :param contract: 
    :param pay_orders:
    :return: list -> 납부회차 객체
    """
    return [o for o in pay_orders if is_due(get_due_date_per_order(contract, o, pay_orders))]


class PdfExportBill(View):
    """고지서 리스트"""

    def get(self, request):
        """
        :: PDF 파일 생성 함수
        :parma request:
        :return:
        """
        project = request.GET.get('project')  # 프로젝트 ID
        issue_date = datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
        np = True if request.GET.get('np') else False
        nl = True if request.GET.get('nl') else False

        context = {
            'issue_date': issue_date,
            'bill_info': SalesBillIssue.objects.get(project=project)
        }  # 전체 데이터 딕셔너리
        inspay_order = InstallmentPaymentOrder.objects.filter(project=project)  # 전체 납부회차 리스트
        now_due_order = context['bill_info'].now_payment_order.pay_code \
            if context['bill_info'].now_payment_order else 2  # 당회 납부 회차

        contractor_list = request.GET.get('seq').split('-')  # 계약 건 ID 리스트

        # 해당 계약건에 대한 데이터 정리 --------------------------------------- start

        context['data_list'] = (self.get_bill_data(cont_id, inspay_order, now_due_order, issue_date, np, nl) \
                                for cont_id in contractor_list)

        # 해당 계약건에 대한 데이터 정리 --------------------------------------- end

        html_string = render_to_string('pdf/bill_control.html', context)
        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/mypdf.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="payment_bill({len(contractor_list)}).pdf"'
            return response

    def get_bill_data(self, cont_id, inspay_order, now_due_order, issue_date, np, nl):
        """
        :: 계약 건 당 전달 데이터 생성 함수
        :param cont_id: 계약자 아이디
        :param inspay_order: 전체 납부 회차
        :param now_due_order: 금회 납부 회차
        :param issue_date: 발행일
        :param np: no price 가격 미표시 여부
        :param nl: no late 연체 미표시 여부
        :return dict(bill_data: 계약 건당 데이터):
        """
        bill_data = {}  # 현재 계약 정보 딕셔너리

        # 계약 건 객체
        bill_data['contract'] = contract = get_contract(cont_id)

        try:
            unit = contract.keyunit.houseunit
        except ObjectDoesNotExist:
            unit = None

        # 동호수
        bill_data['unit'] = unit

        # 이 계약 건 분양가 (계약금, 중도금, 잔금 약정액)
        cont_price = contract.contractprice
        price = cont_price.price
        price_build = cont_price.price_build
        price_land = cont_price.price_land
        price_tax = cont_price.price_tax
        down = cont_price.down_pay
        middle = cont_price.middle_pay
        remain = cont_price.remain_pay

        bill_data['price'] = price if unit else '동호 지정 후 고지'  # 이 건 분양가격
        bill_data['price_build'] = price_build if unit else '-'  # 이 건 건물가
        bill_data['price_land'] = price_land if unit else '-'  # 이 건 대지가
        bill_data['price_tax'] = price_tax if unit else '-'  # 이 건 부가세

        # 납부목록, 완납금액 구하기 ------------------------------------------
        paid_list, paid_sum_total = self.get_paid(contract)
        # --------------------------------------------------------------

        # 해당 계약 건의 회차별 관련 정보
        amount = {'1': down, '2': middle, '3': remain}
        orders_info = self.get_orders_info(inspay_order, amount, paid_sum_total)
        # 완납 회차
        paid_code = self.get_paid_code(orders_info, paid_sum_total)

        # ■ 계약 내용 -----------------------------------------------------
        bill_data['cont_content'] = self.get_cont_content(contract, unit)

        # ■ 납부대금 안내 ----------------------------------------------
        bill_data['this_pay_info'] = self.get_this_pay_info(contract,
                                                            orders_info,
                                                            inspay_order,
                                                            now_due_order,
                                                            paid_code)

        # 납부대금 합계
        bill_data['this_pay_sum'] = {
            'amount_sum': sum([pi["amount"] for pi in bill_data['this_pay_info']]),
            'unpaid_sum': sum([pi["unpaid"] for pi in bill_data['this_pay_info']]),
            'penalty_sum': sum([pi["penalty"] for pi in bill_data['this_pay_info']]),
            'amount_total': sum([pi["sum_amount"] for pi in bill_data['this_pay_info']]),
        }

        # ■ 납부방법 안내 ------------------------------------------------
        pm_cost_sum = sum([pm['pm_cost_sum'] for pm in orders_info])
        bill_data['pay_method'] = (bill_data['this_pay_sum']['amount_total'], pm_cost_sum)

        # ■ 납부약정 및 납입내역 -------------------------------------------
        bill_data['due_orders'] = self.get_due_orders(contract, orders_info,
                                                      inspay_order, now_due_order,
                                                      paid_code, issue_date, is_late_fee=False)

        bill_data['remain_orders'] = self.get_remain_orders(contract, orders_info,
                                                            inspay_order, now_due_order)

        bill_data['paid_sum_total'] = paid_sum_total
        bill_data['late_fee_sum'] = self.get_due_orders(contract, orders_info,
                                                        inspay_order, now_due_order,
                                                        paid_code, issue_date, is_late_fee=True)

        # 표시 정보 제한 여부
        bill_data['no_price'] = np
        bill_data['no_late'] = nl

        # 공백 개수 구하기
        unpaid_count = len(bill_data['this_pay_info'])
        rem_count = len(bill_data['remain_orders'])

        bill_data['blank_line'] = self.get_blank_line(unpaid_count,
                                                      pm_cost_sum,
                                                      inspay_order.count())

        # --------------------------------------------------------------
        return bill_data

    @staticmethod
    def get_paid(contract):
        """
        :: ■ 기 납부금액 구하기
        :param contract: 계약정보
        :return list(paid_list: 납부 건 리스트), int(paid_sum_total: 납부 총액):
        """
        paid_list = ProjectCashBook.objects.filter(
            income__isnull=False,
            project_account_d3__in=(1, 4),  # 분(부)담금 or 분양수입금
            contract=contract
        ).order_by('deal_date', 'id')  # 해당 계약 건 납부 데이터

        paid_sum_total = paid_list.aggregate(Sum('income'))['income__sum']  # 완납 총금액
        paid_sum_total = paid_sum_total if paid_sum_total else 0
        return paid_list, paid_sum_total

    @staticmethod
    def get_cont_content(contract, unit):
        """
        :: ■ 계약 내용
        :param contract: 계약정보
        :param unit: 동호수 정보
        :return dict(contractor: 계약자명, cont_date: 계약일, cont_no: 계약번호, cont_type: 평형):
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

    @staticmethod
    def get_paid_code(orders_info, paid_sum_total):
        """
        :: 완납 회차 구하기
        :param orders_info: 전체 납부 회차
        :param paid_sum_total: 납부 총액
        :return 완납회차 객체:
        """
        try:
            paid_code = [c['order'].pay_code for c in orders_info if paid_sum_total >= c['sum_pay_amount']][-1]
        except IndexError:  # paid_sum_total 이 1회차에 미치지 못하는 경우 == 계약금 부족 시
            paid_code = 0

        return paid_code

    @staticmethod
    def get_this_pay_info(contract,
                          orders_info, inspay_order,
                          now_due_order, paid_code):
        """
        :: ■ 납부대금 안내
        :param cont_id: 계약자 아이디
        :param orders_info: 회차별 부가정보
        :param inspay_order: 회차 정보
        :param now_due_order: 당회 납부 회차
        :param paid_code: 완납 회차
        :return list(dict(order: 납부회차, due_date: 납부기한, amount: 약정금액, unpaid: 미납금액, penalty: 연체가산금, sum_amount: 납부금액)):
        """
        payment_list = []
        unpaid_orders = inspay_order.filter(pay_code__gt=paid_code,
                                            pay_code__lte=now_due_order)  # 최종 기납부회차 이후부터 납부지정회차 까지 회차그룹
        for order in unpaid_orders:
            ord_info = list(filter(lambda o: o['order'] == order, orders_info))[0]

            amount = ord_info['pay_amount']
            unpaid = ord_info['unpaid_amount']
            penalty = 0

            payment_dict = {
                'order': order,
                'due_date': get_due_date_per_order(contract, order, unpaid_orders),
                'amount': amount,
                'unpaid': unpaid,
                'penalty': penalty,
                'sum_amount': unpaid + penalty
            }
            payment_list.append(payment_dict)

        return payment_list

    def get_due_orders(self, contract, orders_info,
                       inspay_order, now_due_order,
                       paid_code, issue_date, is_late_fee=False):
        """
        :: ■ 납부약정 및 납입내역 - 납입내역
        :param contract: 계약 건
        :param orders_info: 납부 회차별 부가정보
        :param inspay_order: 전체 납부회차
        :param now_due_order: 금회 납부 회차
        :param paid_code: 완납회차
        :param issue_date: 발행일자
        :param is_late_fee: 연체료 발행여부
        :return list(paid_list: 왼납 회차 목록):
        """

        # 해당 계약 건 전체 납부 목록 -> [(income, deal_date), ...]
        paid_list = [(p.income, p.deal_date) for p in self.get_paid(contract)[0]]
        paid_date = paid_list[-1][1] if paid_list else None  # 마지막 요소의 deal_date (납부일)

        # 전체 리턴 데이터 목록
        paid_amt_list = []
        due_orders = inspay_order.filter(pay_code__lte=now_due_order)  # 금 회차까지 납부 회차

        excess = 0  # 회차별 초과 납부분
        paid_amt_sum = 0  # 실 수납액 누계

        late_fee_sum = 0

        for order in due_orders:
            due_date = get_due_date_per_order(contract, order, due_orders)  # 납부기한
            ord_info = list(filter(lambda o: o['order'] == order, orders_info))[0]  # 금 회차 orders_info
            amount = ord_info['pay_amount']  # 금 회차 납부 약정액

            paid_amt = 0  # 금회 납부금액

            while True:  # 납입회차별 납입금 구하기
                try:
                    paid = paid_list.pop()  # (income, deal_date) <- 마지막 요소(가장 빠른 납부일자)
                    paid_amt += paid[0]  # 납부액 += income (loop 동안 income 을 모두 더함)
                    paid_date = paid[1]  # 납부일 = deal_date(loop 마지막 납부건 납부일)
                    is_over_amt = (excess + paid_amt) >= amount  # (전회 초과 납부분 + 납부액) >= 약정액
                    # 현재 회차 == 금회 직전 회차 (이 경우 루프 마지막까지 순회하기 위해서 루프탈출 조건에서 제외)
                    is_last_ord = order.pay_code + 1 == now_due_order
                    if is_over_amt and not is_last_ord:  # loop 탈출 조건
                        excess += (paid_amt + excess - amount)  # 금회 초과 납부분 += (금회 납부액 + 전회 초과납부분 - 약정액)
                        break
                except IndexError:  # .pop() 에러 시 탈출
                    break

            paid_date = paid_date if paid_amt else ''
            unpaid_amt = ord_info['unpaid_amount'] if order.pay_code != now_due_order else 0

            if unpaid_amt == 0 or (order.pay_code == 1 and paid_code >= 1):  # 지연금 없거나 1회차 일때 완납코드가 1 이상이면,
                unpaid_days = 0
            else:
                try:
                    unpaid_days = (issue_date - due_date).days
                except Exception:
                    unpaid_days = 0

            delayed_amt = 0  # 당회 납부 지연 시 납부 전 지연금 계산
            delayed_days = 0  # 당회 납부 지연 시 납부 전 지연금 지연일 계산

            paid_amt_sum += paid_amt

            if order.pay_code > 1 and paid_amt and paid_date > due_date:
                sum_p_amt = ord_info['sum_pay_amount']  # 금 회차 납부 약정액
                sum_p_paid = paid_amt_sum - paid_amt
                delayed_amt = sum_p_amt - sum_p_paid if sum_p_amt - sum_p_paid > 0 else 0
                if delayed_amt > 0:
                    delayed_days = (paid_date - due_date).days

            late_fee_sum += self.get_late_fee(unpaid_amt, unpaid_days)[0] + \
                            self.get_late_fee(delayed_amt, delayed_days)[0]

            paid_dict = {
                'order': order.pay_name,
                'due_date': due_date,
                'amount': amount,
                'paid_date': paid_date,
                'paid_amt': paid_amt,
                'unpaid_amt': unpaid_amt,
                'unpaid_days': unpaid_days,
                'unpaid_result': self.get_late_fee(unpaid_amt, unpaid_days),
                'delayed_amt': delayed_amt,
                'delayed_days': delayed_days,
                'delayed_result': self.get_late_fee(delayed_amt, delayed_days),
                'note': f'(+)' if unpaid_days and delayed_days else '',
            }
            paid_amt_list.append(paid_dict)

        if is_late_fee:
            return late_fee_sum
        else:
            return paid_amt_list

    @staticmethod
    def get_remain_orders(contract, orders_info, inspay_order, now_due_order):
        """
        :: ■ 납부약정 및 납입내역 - 잔여회차
        :param contract: 계약 건
        :param orders_info: 납부 회차별 부가정보
        :param inspay_order: 전체 납부 회차
        :param now_due_order: 금회 납부 회차
        :return list(dict(remain_amt_list)): 잔여 회차(dict) 목록:
        """
        remain_amt_list = []
        remain_orders = inspay_order.filter(pay_code__gt=now_due_order)

        for order in remain_orders:
            ord_info = list(filter(lambda o: o['order'] == order, orders_info))[0]
            amount = ord_info['pay_amount']

            paid_dict = {
                'order': order.pay_name,
                'due_date': get_due_date_per_order(contract, order, remain_orders),
                'amount': amount,
                'paid_date': '',
                'paid_amt': 0,
                'delayed_amt': 0,
                'penalty_days': 0,
                'panalty_amt': 0,
            }
            remain_amt_list.append(paid_dict)

        return remain_amt_list

    @staticmethod
    def get_orders_info(inspay_order, amount, paid_sum_total):
        """
        :: 회차별 부가정보
        :param inspay_order: 회차 정보
        :param amount: 전체 약정액 리스트
        :param paid_sum_total: 기 납부 총액
        :return list(dict(order_info_list)): 회차별 부가정보 딕셔너리 리스트
        """
        order_info_list = []
        sum_pay_amount = 0  # 회당 납부 약정액 누계
        pm_cost_sum = 0  # PM 용역비 합계

        for order in inspay_order:
            info = {'order': order}
            pay_amount = amount[order.pay_sort]  # 회당 납부 약정액
            info['pay_amount'] = pay_amount  # 회당 납부 약정액
            sum_pay_amount += pay_amount  # 회당 납부 약정액 누계
            info['sum_pay_amount'] = sum_pay_amount  # 회당 납부 약정액 누계
            unpaid = sum_pay_amount - paid_sum_total  # 약정액 누계 - 총 납부액
            unpaid = unpaid if unpaid > 0 else 0  # 음수(초과 납부 시)는 0 으로 설정
            info['unpaid_amount'] = unpaid if unpaid < pay_amount else pay_amount  # 미납액
            pm_cost_sum += pay_amount if order.is_pm_cost else 0  # PM 용역비 합계
            info['pm_cost_sum'] = pm_cost_sum  # PM 용역비 합계

            order_info_list.append(info)

        return order_info_list

    @staticmethod
    def get_late_fee(late_amt, days):
        """
        :: 회차별 지연 가산금 계산 함수
        :param late_amt: 지연금액
        :param days: 지연일수
        :return int(floor_fee: 가산금), str(적용 이자율):
        """
        rate = 0
        if days < 30:
            rate = 0.08
        elif days <= 90:
            rate = 0.1
        elif days <= 180:
            rate = 0.11
        else:
            rate = 0.12

        floor_fee = int(late_amt * days * rate / 365000) * 1000

        return floor_fee, f'{int(rate * 100)}%'

    @staticmethod
    def get_blank_line(unpaid_count, pm, total_orders_count):
        """
        :: 공백 라인 개수 구하기
        :param unpaid_count: 미납내역 개수
        :param pm: pm 용역비 적용여부
        :param total_orders_count: 전체 납부회차 개수
        :return str(. * 공백라인 수):
        """
        num = unpaid_count + 1 if pm else unpaid_count
        blank_line = (14 - (num + total_orders_count))
        return '.' * blank_line


class PdfExportPayments(View):

    def get(self, request):
        context = dict()

        project = request.GET.get('project')  # 프로젝트 ID
        # 계약 건 객체
        cont_id = request.GET.get('contract')
        context['contract'] = contract = get_contract(cont_id)
        context['pdfSelect'] = request.GET.get('sel')

        pay_orders = InstallmentPaymentOrder.objects.filter(project=project)  # 전체 납부회차 컬렉션

        try:
            unit = contract.keyunit.houseunit
        except ObjectDoesNotExist:
            unit = None

        # 동호수
        context['unit'] = unit

        # 1. 이 계약 건 분양가격 (계약금, 중도금, 잔금 약정액)
        cont_price = contract.contractprice  # 공급가격
        price = cont_price.price
        price_build = cont_price.price_build
        price_land = cont_price.price_land
        price_tax = cont_price.price_tax
        context['price'] = price if unit else '동호 지정 후 고지'  # 이 건 분양가격
        context['price_build'] = price_build if unit else '-'  # 이 건 건물가
        context['price_land'] = price_land if unit else '-'  # 이 건 대지가
        context['price_tax'] = price_tax if unit else '-'  # 이 건 부가세

        down = cont_price.down_pay  # 계약금
        middle = cont_price.middle_pay  # 중도금
        remain = cont_price.remain_pay  # 잔금
        amount = {'1': down, '2': middle, '3': remain}

        # 2. 요약 테이블 데이터
        context['due_amount'] = get_due_amount(pay_orders, contract, amount)  # 약정금 누계
        context['now_order'] = max([(o.pay_code, o.alias_name) for o in get_due_orders(contract, pay_orders)])
        # 2. 간단 차수 정보
        context['simple_orders'] = simple_orders = get_simple_orders(pay_orders, contract, amount)

        # 3. 납부목록, 완납금액 구하기 ------------------------------------------
        paid_dicts, paid_sum_total = get_paid(contract, simple_orders)
        context['paid_dicts'] = paid_dicts
        context['paid_sum_total'] = paid_sum_total  # paid_list.aggregate(Sum('income'))['income__sum']  # 기 납부총액
        # ----------------------------------------------------------------

        html_string = render_to_string('pdf/payments_by_contractor.html', context)

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/mypdf.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="payments_contractor.pdf"'
            return response


class PdfExportCalculation(View):

    def get(self, request):
        context = dict()

        project = request.GET.get('project')  # 프로젝트 ID
        # 계약 건 객체
        cont_id = request.GET.get('contract')
        context['contract'] = contract = get_contract(cont_id)

        pay_orders = SpecialPaymentOrder.objects.filter(project=project)  # 전체 납부회차 컬렉션

        try:
            unit = contract.keyunit.houseunit
        except ObjectDoesNotExist:
            unit = None

        # 동호수
        context['unit'] = unit

        # 1. 이 계약 건 분양가격 (계약금, 중도금, 잔금 약정액)
        cont_price = contract.contractprice  # 공급가격
        price = cont_price.price
        price_build = cont_price.price_build
        price_land = cont_price.price_land
        price_tax = cont_price.price_tax
        context['price'] = price if unit else '동호 지정 후 고지'  # 이 건 분양가격
        context['price_build'] = price_build if unit else '-'  # 이 건 건물가
        context['price_land'] = price_land if unit else '-'  # 이 건 대지가
        context['price_tax'] = price_tax if unit else '-'  # 이 건 부가세

        down1 = self.get_down_pay(contract)[0]  # cont_price.down_pay  # 계약금
        down2 = self.get_down_pay(contract)[1]  # cont_price.down_pay  # 계약금
        amount = {'1': down1, '2': down2}

        # 2. 요약 테이블 데이터
        context['due_amount'] = (down1 * 4) + down2  # 약정금 누계
        context['now_order'] = max([(o.pay_code, o.alias_name) for o in get_due_orders(contract, pay_orders)])
        # 2. 간단 차수 정보
        context['simple_orders'] = simple_orders = self.get_past_orders(pay_orders, contract, amount)

        # 3. 납부목록, 완납금액 구하기 ------------------------------------------
        paid_dicts, paid_sum_total = get_paid(contract, simple_orders, True)
        context['paid_dicts'] = paid_dicts
        context['paid_sum_total'] = paid_sum_total  # paid_list.aggregate(Sum('income'))['income__sum']  # 기 납부총액
        # ----------------------------------------------------------------

        html_string = render_to_string('pdf/calculation_by_contractor.html', context)

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/mypdf.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="calculation_contractor.pdf"'
            return response

    @staticmethod
    def get_down_pay(contract):
        down = SpecialDownPay.objects.get(order_group=contract.order_group, unit_type=contract.unit_type)
        return down.payment_amount, down.payment_remain

    @staticmethod
    def get_past_orders(pay_orders, contract, amount):
        """
        :: 약식 납부회차 구하기
        :param pay_orders:
        :param contract:
        :param amount:
        :return: dict 형식 납부회차 리스트
        """

        simple_orders = []

        amount_total = 0
        for order in pay_orders:
            amount_total += amount[order.pay_sort]  # 회차별 계약금 누계
            ord_info = {
                'name': order.alias_name if order.alias_name else order.pay_name,  # 회차별 별칭
                'due_date': get_due_date_per_order(contract, order, pay_orders),  # 회차별 납부기한
                'amount1': amount['1'],  # 회차별 계약금
                'amount2': amount['2'],  # 나머지 계약금
                'amount_total': amount_total,  # 회차별 계약금 누계
            }
            simple_orders.append(ord_info)

        return simple_orders
