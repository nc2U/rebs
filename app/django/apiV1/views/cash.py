from datetime import datetime
from django.db.models import Sum, Count, F, Q, Case, When
from rest_framework import viewsets
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

TODAY = datetime.today().strftime('%Y-%m-%d')


# Cash --------------------------------------------------------------------------
class BankCodeViewSet(viewsets.ModelViewSet):
    queryset = BankCode.objects.all()
    pagination_class = PageNumberPaginationFifty
    serializer_class = BankCodeSerializer


class ComBankAccountViewSet(viewsets.ModelViewSet):
    queryset = CompanyBankAccount.objects.all()
    serializer_class = CompanyBankAccountSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BalanceByAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceByAccountSerializer
    pagination_class = PageNumberPaginationOneHundred
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('company',)

    def get_queryset(self):
        date = self.request.query_params.get('date')
        date = date if date else TODAY

        queryset = CashBook.objects.all() \
            .order_by('bank_account') \
            .filter(is_separate=False, deal_date__lte=date)

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


class CashBookViewSet(viewsets.ModelViewSet):
    queryset = CashBook.objects.all()
    serializer_class = CashBookSerializer
    pagination_class = PageNumberPaginationFifteen
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_class = CashBookFilterSet
    search_fields = ('content', 'trader', 'note')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DateCashBookViewSet(CashBookViewSet):
    pagination_class = PageNumberPaginationTwoHundred

    def get_queryset(self):
        date = self.request.query_params.get('date')
        date = date if date else TODAY
        return CashBook.objects.filter(is_separate=False, deal_date__exact=date).order_by('deal_date', 'created_at',
                                                                                          'id')


class ProjectBankAccountViewSet(viewsets.ModelViewSet):
    queryset = ProjectBankAccount.objects.all()
    serializer_class = ProjectBankAccountSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)


class PrBalanceByAccountViewSet(viewsets.ModelViewSet):
    serializer_class = PrBalanceByAccountSerializer
    pagination_class = PageNumberPaginationOneHundred
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)

    def get_queryset(self):
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
                  'bank_account', 'is_contract_payment', 'contract', 'contract__order_group',
                  'contract__unit_type', 'no_contract')


class ProjectCashBookViewSet(viewsets.ModelViewSet):
    queryset = ProjectCashBook.objects.filter(Q(is_imprest=False) | Q(project_account_d2=63, income__isnull=True))
    serializer_class = ProjectCashBookSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    pagination_class = PageNumberPaginationFifteen
    filterset_class = ProjectCashBookFilterSet
    search_fields = ('contract__contractor__name', 'content', 'trader', 'note')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectDateCashBookViewSet(ProjectCashBookViewSet):
    pagination_class = PageNumberPaginationTwoHundred

    def get_queryset(self):
        date = self.request.query_params.get('date')
        date = date if date else TODAY
        return ProjectCashBook.objects.filter(is_separate=False, deal_date__exact=date).order_by('deal_date',
                                                                                                 'created_at', 'id')


class ProjectImprestViewSet(ProjectCashBookViewSet):
    queryset = ProjectCashBook.objects.filter(is_imprest=True).exclude(project_account_d2=63, income__isnull=True)


class PaymentViewSet(ProjectCashBookViewSet):
    serializer_class = PaymentSerializer
    pagination_class = PageNumberPaginationTen

    def get_queryset(self):
        return ProjectCashBook.objects.filter(project_account_d2__in=(1, 2), refund_contractor=None)


class AllPaymentViewSet(PaymentViewSet):
    pagination_class = PageNumberPaginationOneHundred


class PaymentSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSummarySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)

    def get_queryset(self):
        return ProjectCashBook.objects.filter(contract__activation=True, contract__contractor__status=2) \
            .order_by('contract__unit_type') \
            .annotate(unit_type=F('contract__unit_type')) \
            .values('unit_type') \
            .annotate(type_total=Sum('income'))


class ContNumByTypeViewSet(viewsets.ModelViewSet):
    serializer_class = NumContractByTypeSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)

    def get_queryset(self):
        return Contract.objects.filter(activation=True, contractor__status=2) \
            .values('unit_type') \
            .annotate(num_cont=Count('unit_type'))


class SalesPriceViewSet(viewsets.ModelViewSet):
    # name = 'price-list'
    queryset = SalesPriceByGT.objects.all()
    serializer_class = SalesPriceSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project', 'order_group', 'unit_type')


class InstallmentOrderViewSet(viewsets.ModelViewSet):
    queryset = InstallmentPaymentOrder.objects.all()
    serializer_class = InstallmentOrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    pagination_class = PageNumberPaginationTwenty
    filterset_fields = ('project', 'pay_sort', 'is_pm_cost')
    search_fields = ('pay_name', 'alias_name')


class DownPaymentViewSet(viewsets.ModelViewSet):
    queryset = DownPayment.objects.all()
    serializer_class = DownPaymentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    pagination_class = PageNumberPaginationTwenty
    filterset_fields = ('project', 'order_group', 'unit_type')

# class OverDueRuleViewSet(viewsets.ModelViewSet):
#     queryset = OverDueRule.objects.all()
#     serializer_class = OverDueRuleSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
