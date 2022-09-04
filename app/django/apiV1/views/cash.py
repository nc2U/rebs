from datetime import datetime
from django.db.models import Sum, Count, F, Q, Case, When
from rest_framework import generics, viewsets
from django_filters.rest_framework import FilterSet
from django_filters import DateFilter, BooleanFilter

from ..permission import *
from ..pagination import *
from ..serializers.cash import *

from cash.models import (BankCode, CompanyBankAccount, ProjectBankAccount,
                         CashBook, ProjectCashBook, SalesPriceByGT,
                         InstallmentPaymentOrder, DownPayment, OverDueRule)
from contract.models import (OrderGroup, Contract, Contractor,
                             ContractorAddress, ContractorContact, ContractorRelease)


# Cash --------------------------------------------------------------------------
class BankCodeList(generics.ListAPIView):
    name = 'bankcode-list'
    queryset = BankCode.objects.all()
    pagination_class = PageNumberPaginationFifty
    serializer_class = BankCodeSerializer


class BankCodeDetail(generics.ListAPIView):
    name = 'bankcode-detail'
    queryset = BankCode.objects.all()
    serializer_class = BankCodeSerializer


class ComBankAccountViewSets(viewsets.ModelViewSet):
    queryset = CompanyBankAccount.objects.all()
    serializer_class = CompanyBankAccountSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BalanceByAccountList(generics.ListAPIView):
    name = 'balance-by-acc'
    serializer_class = BalanceByAccountSerializer
    pagination_class = PageNumberPaginationOneHundred
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('company',)

    def get_queryset(self):
        TODAY = datetime.today().strftime('%Y-%m-%d')
        date = self.request.query_params.get('date')
        date = date if date else TODAY

        queryset = CashBook.objects.all() \
            .order_by('bank_account') \
            .filter(deal_date__lte=date)

        return queryset.annotate(bank_acc=F('bank_account__alias_name')) \
            .values('bank_acc') \
            .annotate(inc_sum=Sum('income'),
                      out_sum=Sum('outlay'),
                      date_inc=Sum(Case(
                          When(deal_date=date, then=F('income')),
                          default=0
                      )),
                      date_out=Sum(Case(
                          When(deal_date=date, then=F('outlay')),
                          default=0
                      )))


class CashBookFilterSet(FilterSet):
    from_deal_date = DateFilter(field_name='deal_date', lookup_expr='gte', label='납부일자부터')
    to_deal_date = DateFilter(field_name='deal_date', lookup_expr='lte', label='납부일자까지')

    class Meta:
        model = CashBook
        fields = ('company', 'from_deal_date', 'to_deal_date', 'sort',
                  'account_d1', 'account_d2', 'account_d3', 'bank_account')


class CashBookList(generics.ListCreateAPIView):
    name = 'cashbook-list'
    queryset = CashBook.objects.all()
    serializer_class = CashBookSerializer
    pagination_class = PageNumberPaginationFifteen
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_class = CashBookFilterSet
    search_fields = ('content', 'trader', 'note')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DateCashBookList(CashBookList):
    name = 'date-cashbook'
    pagination_class = PageNumberPaginationTwoHundred

    def get_queryset(self):
        TODAY = datetime.today().strftime('%Y-%m-%d')
        date = self.request.query_params.get('date')
        date = date if date else TODAY
        return CashBook.objects.filter(deal_date__exact=date)


class CashBookDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'cashbook-detail'
    queryset = CashBook.objects.all()
    serializer_class = CashBookSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ProjectBankAccountList(generics.ListCreateAPIView):
    name = 'project_bank-list'
    queryset = ProjectBankAccount.objects.all()
    serializer_class = ProjectBankAccountSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)


class ProjectBankAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'project_bank-detail'
    queryset = ProjectBankAccount.objects.all()
    serializer_class = ProjectBankAccountSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class PrBalanceByAccountList(generics.ListAPIView):
    name = 'pr-balance-by-acc'
    serializer_class = PrBalanceByAccountSerializer
    pagination_class = PageNumberPaginationOneHundred
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def get_queryset(self):
        TODAY = datetime.today().strftime('%Y-%m-%d')
        date = self.request.query_params.get('date')
        date = date if date else TODAY

        queryset = ProjectCashBook.objects.all() \
            .order_by('bank_account') \
            .filter(is_separate=False,
                    bank_account__directpay=False,
                    deal_date__lte=date)

        return queryset.annotate(bank_acc=F('bank_account__alias_name')) \
            .values('bank_acc') \
            .annotate(inc_sum=Sum('income'),
                      out_sum=Sum('outlay'),
                      date_inc=Sum(Case(
                          When(deal_date=date, then=F('income')),
                          default=0
                      )),
                      date_out=Sum(Case(
                          When(deal_date=date, then=F('outlay')),
                          default=0
                      )))


class ProjectCashBookFilterSet(FilterSet):
    from_deal_date = DateFilter(field_name='deal_date', lookup_expr='gte', label='납부일자부터')
    to_deal_date = DateFilter(field_name='deal_date', lookup_expr='lte', label='납부일자까지')
    no_contract = BooleanFilter(field_name='contract', lookup_expr='isnull', label='미등록')

    class Meta:
        model = ProjectCashBook
        fields = ('project', 'sort', 'project_account_d1', 'project_account_d2',
                  'from_deal_date', 'to_deal_date', 'deal_date', 'installment_order',
                  'bank_account', 'is_contract_payment', 'contract', 'no_contract')


class ProjectCashBookList(generics.ListCreateAPIView):
    name = 'project_cashbook-list'
    queryset = ProjectCashBook.objects.filter(Q(is_imprest=False) | Q(project_account_d2=63, income__isnull=True))
    serializer_class = ProjectCashBookSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    pagination_class = PageNumberPaginationFifteen
    filter_class = ProjectCashBookFilterSet
    search_fields = ('contract__contractor__name', 'content', 'trader', 'note')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectDateCashBookList(ProjectCashBookList):
    name = 'pr-date-cashbook'
    pagination_class = PageNumberPaginationTwoHundred

    def get_queryset(self):
        TODAY = datetime.today().strftime('%Y-%m-%d')
        date = self.request.query_params.get('date')
        date = date if date else TODAY
        return ProjectCashBook.objects.filter(is_separate=False, deal_date__exact=date)


class ProjectImprestList(ProjectCashBookList):
    name = 'project-imprest-list'
    queryset = ProjectCashBook.objects.filter(is_imprest=True).exclude(project_account_d2=63, income__isnull=True)


class ProjectCashBookDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'project_cashbook-detail'
    queryset = ProjectCashBook.objects.all()
    serializer_class = ProjectCashBookSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class PaymentList(ProjectCashBookList):
    name = 'payment-list'
    serializer_class = PaymentSerializer
    pagination_class = PageNumberPaginationTen

    def get_queryset(self):
        return ProjectCashBook.objects.filter(project_account_d2__in=(1, 2), refund_contractor=None)


class AllPaymentList(PaymentList):
    name = 'all-payment-list'
    pagination_class = PageNumberPaginationOneHundred


class PaymentSummary(generics.ListAPIView):
    name = 'payment-sum'
    serializer_class = PaymentSummarySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def get_queryset(self):
        return ProjectCashBook.objects.filter(contract__activation=True, contract__contractor__status=2) \
            .order_by('contract__unit_type') \
            .annotate(unit_type=F('contract__unit_type')) \
            .values('unit_type') \
            .annotate(type_total=Sum('income'))


class NumContractByType(generics.ListAPIView):
    name = 'cont-count'
    serializer_class = NumContractByTypeSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def get_queryset(self):
        return Contract.objects.filter(activation=True, contractor__status=2) \
            .values('unit_type') \
            .annotate(num_cont=Count('unit_type'))


class SalesPriceList(generics.ListCreateAPIView):
    name = 'price-list'
    queryset = SalesPriceByGT.objects.all()
    serializer_class = SalesPriceSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project', 'order_group', 'unit_type')


class SalesPriceDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'price-detail'
    queryset = SalesPriceByGT.objects.all()
    serializer_class = SalesPriceSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class InstallmentOrderList(generics.ListCreateAPIView):
    name = 'install_order-list'
    queryset = InstallmentPaymentOrder.objects.all()
    serializer_class = InstallmentOrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    pagination_class = PageNumberPaginationTwenty
    filter_fields = ('project', 'pay_sort', 'is_pm_cost')
    search_fields = ('pay_name', 'alias_name')


class InstallmentOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'install_order-detail'
    queryset = InstallmentPaymentOrder.objects.all()
    serializer_class = InstallmentOrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class DownPaymentList(generics.ListCreateAPIView):
    name = 'downpay-list'
    queryset = DownPayment.objects.all()
    serializer_class = DownPaymentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    pagination_class = PageNumberPaginationTwenty
    filter_fields = ('project', 'order_group', 'unit_type')


class DownPaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'downpay-detail'
    queryset = DownPayment.objects.all()
    serializer_class = DownPaymentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

# class OverDueRuleList(generics.ListCreateAPIView):
#     name = 'over_due_rule-list'
#     queryset = OverDueRule.objects.all()
#     serializer_class = OverDueRuleSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class OverDueRuleDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'over_due_rule-detail'
#     queryset = OverDueRule.objects.all()
#     serializer_class = OverDueRuleSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
