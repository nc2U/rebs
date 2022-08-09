from datetime import datetime
from django.db.models import Sum, Count, F, Q, Case, When
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import FilterSet
from django_filters import ChoiceFilter, ModelChoiceFilter, DateFilter, BooleanFilter

from .permission import *
from .pagination import *
from .serializers import *

from accounts.models import User, Profile, Todo
from company.models import Company, Logo, Department, Position, Staff
from project.models import (Project, UnitType, UnitFloorType,
                            KeyUnit, BuildingUnit, HouseUnit, ProjectBudget,
                            Site, SiteOwner, SiteOwnshipRelationship, SiteContract)
from rebs.models import (AccountSort, AccountSubD1, AccountSubD2, AccountSubD3, ProjectAccountSort,
                         ProjectAccountD1, ProjectAccountD2, CalendarSchedule, WiseSaying)
from cash.models import (BankCode, CompanyBankAccount, ProjectBankAccount,
                         CashBook, ProjectCashBook, SalesPriceByGT,
                         InstallmentPaymentOrder, DownPayment, OverDueRule)
from contract.models import (OrderGroup, Contract, Contractor,
                             ContractorAddress, ContractorContact, ContractorRelease)
from notice.models import SalesBillIssue
from document.models import Group, Board, Category, LawsuitCase, Post, Image, Link, File, Comment, Tag


class ApiIndex(generics.GenericAPIView):
    name = 'api-index'
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        api = 'api:'
        return Response({
            'user': reverse(api + 'user-list', request=request),
            'profile': reverse(api + 'profile-list', request=request),
            'todo': reverse(api + 'todo-list', request=request),
            'company': reverse(api + 'company-list', request=request),
            'logo': reverse(api + 'logo-list', request=request),
            'department': reverse(api + 'depart-list', request=request),
            'position': reverse(api + 'position-list', request=request),
            'staff': reverse(api + 'staff-list', request=request),
            'schedule': reverse(api + 'schedule-list', request=request),
            'account-sort': reverse(api + AccountSortList.name, request=request),
            'account-depth1': reverse(api + AccountSubD1List.name, request=request),
            'account-depth2': reverse(api + AccountSubD2List.name, request=request),
            'account-depth3': reverse(api + AccountSubD3List.name, request=request),
            'project-acc-sort': reverse(api + ProjectAccountSortList.name, request=request),
            'project-acc-d1': reverse(api + ProjectAccountD1List.name, request=request),
            'project-acc-d2': reverse(api + ProjectAccountD2List.name, request=request),
            'project': reverse(api + 'project-list', request=request),
            'type': reverse(api + 'unittype-list', request=request),
            'floor': reverse(api + 'floortype-list', request=request),
            'key-unit': reverse(api + 'key_unit-list', request=request),
            'bldg-unit': reverse(api + 'bldg-list', request=request),
            'house-unit': reverse(api + HouseUnitList.name, request=request),
            'available-house-unit': reverse(api + AvailableHouseUnitList.name, request=request),
            'all-house-unit': reverse(api + AllHouseUnitList.name, request=request),
            'budget': reverse(api + ProjectBudgetList.name, request=request),
            'exec-amount-budget': reverse(api + ExecAmountToBudgetList.name, request=request),
            # 'site': reverse(api + SiteList.name, request=request),
            # 'site-owner': reverse(api + SiteOwnerList.name, request=request),
            # 'site-relation': reverse(api + RelationList.name, request=request),
            # 'site-contract': reverse(api + SiteContractList.name, request=request),
            # 'bank-code': reverse(api + BankCodeList.name, request=request),
            'com-bank': reverse(api + 'com_bank-list', request=request),
            'balance-by-acc': reverse(api + BalanceByAccountList.name, request=request),
            'cashbook': reverse(api + CashBookList.name, request=request),
            'date-cashbook': reverse(api + DateCashBookList.name, request=request),
            'project-bank': reverse(api + ProjectBankAccountList.name, request=request),
            'pr-balance-by-acc': reverse(api + PrBalanceByAccountList.name, request=request),
            'pr-date-cashbook': reverse(api + ProjectDateCashBookList.name, request=request),
            'project-cashbook': reverse(api + ProjectCashBookList.name, request=request),
            'project-imprest': reverse(api + ProjectImprestList.name, request=request),
            'payment-list': reverse(api + PaymentList.name, request=request),
            'all-payment-list': reverse(api + AllPaymentList.name, request=request),
            'payment-sum': reverse(api + PaymentSummary.name, request=request),
            'cont-count': reverse(api + NumContractByType.name, request=request),
            'price': reverse(api + SalesPriceList.name, request=request),
            'pay-order': reverse(api + InstallmentOrderList.name, request=request),
            'down-payment': reverse(api + DownPaymentList.name, request=request),
            # 'over-due-rule': reverse(api + OverDueRuleList.name, request=request),
            'order-group': reverse(api + OrderGroupList.name, request=request),
            'contract': reverse(api + ContractList.name, request=request),
            'contract-custom-list': reverse(api + ContractCustomList.name, request=request),
            'subs-sum': reverse(api + SubsSummaryList.name, request=request),
            'cont-sum': reverse(api + ContSummaryList.name, request=request),
            'contractor': reverse(api + ContractorList.name, request=request),
            'contractor-address': reverse(api + ContAddressList.name, request=request),
            'contractor-contact': reverse(api + ContContactList.name, request=request),
            'contractor-release': reverse(api + ContReleaseList.name, request=request),
            'sales-bill-issue': reverse(api + BillIssueList.name, request=request),
            # 'group': reverse(api + GroupList.name, request=request),
            # 'board': reverse(api + BoardList.name, request=request),
            # 'category': reverse(api + CategoryList.name, request=request),
            # 'suitcase': reverse(api + LawSuitCaseList.name, request=request),
            # 'post': reverse(api + PostList.name, request=request),
            # 'image': reverse(api + ImageList.name, request=request),
            # 'link': reverse(api + LinkList.name, request=request),
            # 'file': reverse(api + FileList.name, request=request),
            # 'comment': reverse(api + CommentList.name, request=request),
            # 'tag': reverse(api + TagList.name, request=request),
            'wise-say': reverse(api + WiseSayList.name, request=request),
        })


# Accounts --------------------------------------------------------------------------
class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnSelfOrReadOnly)


class ProfileViewSets(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoViewSets(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly)
    filter_fields = ('user', 'soft_deleted')
    search_fields = ('title',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Company --------------------------------------------------------------------------
class CompanyViewSets(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class LogoViewSets(viewsets.ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class DepartmentViewSets(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class PositionViewSets(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class StaffViewSets(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CalendarScheduleViewSet(viewsets.ModelViewSet):
    queryset = CalendarSchedule.objects.all()
    serializer_class = CalendarScheduleSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    pagination_class = PageNumberPaginationOneHundred
    search_fields = ('start_date', 'start_time', 'end_date', 'end_time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Rebs --------------------------------------------------------------------------
class AccountSortList(generics.ListAPIView):
    name = 'acc_sort-list'
    queryset = AccountSort.objects.all()
    serializer_class = AccountSortSerializer


class AccountSubD1List(generics.ListAPIView):
    name = 'acc_d1-list'
    queryset = AccountSubD1.objects.all()
    serializer_class = AccountSubD1Serializer
    filter_fields = ('accountsort',)


class AccountSubD2List(generics.ListAPIView):
    name = 'acc_d2-list'
    queryset = AccountSubD2.objects.all()
    serializer_class = AccountSubD2Serializer
    pagination_class = PageNumberPaginationTwenty
    filter_fields = ('d1__accountsort', 'd1')


class AccountSubD3List(generics.ListAPIView):
    name = 'acc_d3-list'
    queryset = AccountSubD3.objects.all()
    serializer_class = AccountSubD3Serializer
    pagination_class = PageNumberPaginationTwoHundred
    filter_fields = ('d2__d1__accountsort', 'd2__d1', 'd2')


class ProjectAccountSortList(generics.ListAPIView):
    name = 'pro-acc_sort-list'
    queryset = ProjectAccountSort.objects.all()
    serializer_class = AccountSortSerializer


class ProjectAccountD1List(generics.ListAPIView):
    name = 'project_acc_d1-list'
    queryset = ProjectAccountD1.objects.all()
    pagination_class = PageNumberPaginationTwenty
    serializer_class = ProjectAccountD1Serializer
    filter_fields = ('projectaccountsort',)


class ProjectAccountD2List(generics.ListAPIView):
    name = 'project_acc_d2-list'
    queryset = ProjectAccountD2.objects.all()
    pagination_class = PageNumberPaginationOneHundred
    serializer_class = ProjectAccountD2Serializer
    filter_fields = ('d1', 'd1__projectaccountsort')


# Project --------------------------------------------------------------------------
class ProjectViewSets(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class UnitTypeViewSets(viewsets.ModelViewSet):
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)
    search_fields = ('name',)


class UnitFloorTypeViewSets(viewsets.ModelViewSet):
    queryset = UnitFloorType.objects.all()
    serializer_class = UnitFloorTypeSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)
    search_fields = ('alias_name',)


class KeyUnitListFilterSet(FilterSet):
    available = BooleanFilter(field_name='contract', lookup_expr='isnull', label='계약가능유닛')

    class Meta:
        model = KeyUnit
        fields = ('project', 'unit_type', 'contract', 'available')


class KeyUnitViewSets(viewsets.ModelViewSet):
    queryset = KeyUnit.objects.all()
    serializer_class = KeyUnitSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_class = KeyUnitListFilterSet


class BuildingUnitViewSets(viewsets.ModelViewSet):
    queryset = BuildingUnit.objects.all()
    serializer_class = BuildingUnitSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)
    search_fields = ('name',)


class HouseUnitList(generics.ListCreateAPIView):
    name = 'unit-list'
    queryset = HouseUnit.objects.all()
    serializer_class = HouseUnitSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project', 'building_unit')
    search_fields = ('hold_reason',)


class HouseUnitDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'unit-detail'
    queryset = HouseUnit.objects.all()
    serializer_class = HouseUnitSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class AvailableHouseUnitList(HouseUnitList):
    name = 'all-house-unit'

    def get_queryset(self):
        houseunit = HouseUnit.objects.all()
        queryset = houseunit

        project = self.request.query_params.get('project', None)
        unit_type = self.request.query_params.get('unit_type', None)

        if project and unit_type:
            queryset = houseunit.filter(project=project, unit_type=unit_type, key_unit__isnull=True)

        contract = self.request.query_params.get('contract', None)
        if contract is not None:
            queryset = houseunit.filter(
                Q(project=project, unit_type=unit_type, key_unit__isnull=True) |
                Q(key_unit__contract=contract))
        return queryset


class AllHouseUnitList(HouseUnitList):
    name = 'all-unit-list'
    serializer_class = AllHouseUnitSerializer
    pagination_class = PageNumberPaginationThreeThousand


class ProjectBudgetList(generics.ListCreateAPIView):
    name = 'projectbudget-list'
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)


class ExecAmountToBudgetList(generics.ListAPIView):
    name = 'execution-amount'
    serializer_class = ExecAmountToBudget
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def get_queryset(self):
        TODAY = datetime.today().strftime('%Y-%m-%d')
        date = self.request.query_params.get('date')
        date = date if date else TODAY
        month_first = datetime(datetime.strptime(date, '%Y-%m-%d').year,
                               datetime.strptime(date, '%Y-%m-%d').month,
                               1).strftime('%Y-%m-%d')

        queryset = ProjectCashBook.objects.all() \
            .order_by('project_account_d2') \
            .filter(is_separate=False,
                    project_account_d2__d1__gte=6,
                    project_account_d2__d1__lte=10,
                    bank_account__directpay=False,
                    deal_date__lte=date)

        return queryset.annotate(acc_d2=F('project_account_d2')) \
            .values('acc_d2') \
            .annotate(all_sum=Sum('outlay'),
                      month_sum=Sum(Case(
                          When(deal_date__gte=month_first, then=F('outlay')),
                          default=0
                      )))


# class ProjectBudgetDetail(generics.ListCreateAPIView):
#     name = 'projectbudget-detail'
#     queryset = ProjectBudget.objects.all()
#     serializer_class = ProjectBudgetSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class SiteList(generics.ListCreateAPIView):
#     name = 'site-list'
#     queryset = Site.objects.all()
#     serializer_class = SiteSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class SiteDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'site-detail'
#     queryset = Site.objects.all()
#     serializer_class = SiteSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class SiteOwnerList(generics.ListCreateAPIView):
#     name = 'siteowner-list'
#     queryset = SiteOwner.objects.all()
#     serializer_class = SiteOwnerSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class SiteOwnerDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'siteowner-detail'
#     queryset = SiteOwner.objects.all()
#     serializer_class = SiteOwnerSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class RelationList(generics.ListCreateAPIView):
#     name = 'relation-list'
#     queryset = SiteOwnshipRelationship.objects.all()
#     serializer_class = SiteOwnshipRelationSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class RelationDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'relation-detail'
#     queryset = SiteOwnshipRelationship.objects.all()
#     serializer_class = SiteOwnshipRelationSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class SiteContractList(generics.ListCreateAPIView):
#     name = 'sitecontract-list'
#     queryset = SiteContract.objects.all()
#     serializer_class = SiteContractSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class SiteContractDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'sitecontract-detail'
#     queryset = SiteContract.objects.all()
#     serializer_class = SiteContractSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# # Cash --------------------------------------------------------------------------
# class BankCodeList(generics.ListAPIView):
#     name = 'bankcode-list'
#     queryset = BankCode.objects.all()
#     serializer_class = BankCodeSerializer
#
#
# class BankCodeDetail(generics.ListAPIView):
#     name = 'bankcode-detail'
#     queryset = BankCode.objects.all()
#     serializer_class = BankCodeSerializer


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


# Contract --------------------------------------------------------------------------
class OrderGroupList(generics.ListCreateAPIView):
    name = 'order_group-list'
    queryset = OrderGroup.objects.all()
    serializer_class = OrderGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project', 'sort')
    search_fields = ('order_group_name',)


class OrderGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'order_group-detail'
    queryset = OrderGroup.objects.all()
    serializer_class = OrderGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContractFilter(FilterSet):
    keyunit__houseunit__building_unit = ModelChoiceFilter(queryset=BuildingUnit.objects.all(), label='동(건물)')
    contractor__status = ChoiceFilter(field_name='contractor__status', choices=Contractor.STATUS_CHOICES, label='현재상태')
    contractor__is_registed = BooleanFilter(field_name='contractor__is_registed', label='인가등록여부')
    from_contract_date = DateFilter(field_name='contractor__contract_date', lookup_expr='gte', label='계약일자부터')
    to_contract_date = DateFilter(field_name='contractor__contract_date', lookup_expr='lte', label='계약일자까지')

    class Meta:
        model = Contract
        fields = ('project', 'order_group', 'activation', 'unit_type',
                  'keyunit__houseunit__building_unit', 'contractor__status',
                  'contractor__is_registed', 'from_contract_date', 'to_contract_date')


class ContractList(generics.ListCreateAPIView):
    name = 'contract-list'
    queryset = Contract.objects.all()
    serializer_class = ContractListSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_class = ContractFilter
    search_fields = (
        'serial_number', 'contractor__name', 'contractor__note', 'contractor__contractorcontact__cell_phone')
    ordering_fields = (
        'created_at', 'contractor__contract_date', 'serial_number', 'contractor__name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'contract-detail'
    queryset = Contract.objects.all()
    serializer_class = ContractListSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContractCustomList(ContractList):
    name = 'contract-cumstom-list'
    serializer_class = ContractCustomListSerializer


class ContractCustomDetail(ContractDetail):
    name = 'contract-custom-detail'
    serializer_class = ContractCustomListSerializer


class SubsSummaryList(generics.ListAPIView):
    name = 'subs-summary'
    serializer_class = SubsSummarySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def get_queryset(self):
        return Contract.objects.filter(activation=True, contractor__status=1) \
            .values('unit_type') \
            .annotate(num_cont=Count('unit_type'))


class ContSummaryList(generics.ListAPIView):
    name = 'cont-summary'
    serializer_class = ContSummarySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def get_queryset(self):
        return Contract.objects.filter(activation=True, contractor__status=2) \
            .values('order_group', 'unit_type') \
            .annotate(num_cont=Count('order_group'))


class ContractorList(generics.ListCreateAPIView):
    name = 'contractor-list'
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('gender', 'is_registed', 'status')
    search_fields = ('name', 'note', 'contract__serial_number')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContractorDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'contractor-detail'
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContAddressList(generics.ListCreateAPIView):
    name = 'cont_address-list'
    queryset = ContractorAddress.objects.all()
    serializer_class = ContractorAddressSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContAddressDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'cont_address-detail'
    queryset = ContractorAddress.objects.all()
    serializer_class = ContractorAddressSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContContactList(generics.ListCreateAPIView):
    name = 'contact-list'
    queryset = ContractorContact.objects.all()
    serializer_class = ContractorContactSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContContactDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'contact-detail'
    queryset = ContractorContact.objects.all()
    serializer_class = ContractorContactSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContReleaseList(generics.ListCreateAPIView):
    name = 'release-list'
    queryset = ContractorRelease.objects.all().order_by('-request_date')
    serializer_class = ContractorReleaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContReleaseDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'release-detail'
    queryset = ContractorRelease.objects.all()
    serializer_class = ContractorReleaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BillIssueList(generics.ListCreateAPIView):
    name = 'bill_issue-list'
    queryset = SalesBillIssue.objects.all()
    serializer_class = SallesBillIssueSerializer
    filter_fields = ('project',)
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BillIssueDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'bill_issue-detail'
    queryset = SalesBillIssue.objects.all()
    serializer_class = SallesBillIssueSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# # Document --------------------------------------------------------------------------
# class GroupList(generics.ListCreateAPIView):
#     name = 'group-list'
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'group-detail'
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class BoardList(generics.ListCreateAPIView):
#     name = 'board-list'
#     queryset = Board.objects.all()
#     serializer_class = BoardSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'board-detail'
#     queryset = Board.objects.all()
#     serializer_class = BoardSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class CategoryList(generics.ListCreateAPIView):
#     name = 'category-list'
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'category-detail'
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class LawSuitCaseList(generics.ListCreateAPIView):
#     name = 'suitcase-list'
#     queryset = LawsuitCase.objects.all()
#     serializer_class = LawSuitCaseSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class LawSuitCaseDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'suitcase-detail'
#     queryset = LawsuitCase.objects.all()
#     serializer_class = LawSuitCaseSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class PostList(generics.ListCreateAPIView):
#     name = 'post-list'
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'post-detail'
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class ImageList(generics.ListCreateAPIView):
#     name = 'image-list'
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'image-detail'
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class LinkList(generics.ListCreateAPIView):
#     name = 'link-list'
#     queryset = Link.objects.all()
#     serializer_class = LinkSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'link-detail'
#     queryset = Link.objects.all()
#     serializer_class = LinkSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class FileList(generics.ListCreateAPIView):
#     name = 'file-list'
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class FileDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'file-detail'
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class CommentList(generics.ListCreateAPIView):
#     name = 'comment-list'
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'comment-detail'
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# class TagList(generics.ListCreateAPIView):
#     name = 'tag-list'
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class TagDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'tag-detail'
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# Etc --------------------------------------------------------------------------
class WiseSayList(generics.ListCreateAPIView):
    name = 'wise-say-list'
    queryset = WiseSaying.objects.all()
    serializer_class = WiseSaySerializer
    permissions_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class WiseSayDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'wise-say-detail'
    queryset = WiseSaying.objects.all()
    serializer_class = WiseSaySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
