from django.urls import path

from rest_framework.response import Response
from rest_framework.reverse import reverse

from .views.accounts import *
from .views.company import *
from .views.rebs import *
from .views.project import *
from .views.cash import *
from .views.contract import *
from .views.notice import *
from .views.document import *


class ApiIndex(generics.GenericAPIView):
    name = 'apiV1-index'
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        api = 'apiV1:'
        return Response({
            # accounts
            'user': reverse(api + 'user-list', request=request),
            'profile': reverse(api + 'profile-list', request=request),
            'todo': reverse(api + 'todo-list', request=request),
            # company
            'company': reverse(api + 'company-list', request=request),
            'logo': reverse(api + 'logo-list', request=request),
            'department': reverse(api + 'depart-list', request=request),
            'position': reverse(api + 'position-list', request=request),
            'staff': reverse(api + 'staff-list', request=request),
            # rebs
            'schedule': reverse(api + 'schedule-list', request=request),
            'account-sort': reverse(api + AccountSortList.name, request=request),
            'account-depth1': reverse(api + AccountSubD1List.name, request=request),
            'account-depth2': reverse(api + AccountSubD2List.name, request=request),
            'account-depth3': reverse(api + AccountSubD3List.name, request=request),
            'project-acc-sort': reverse(api + ProjectAccountSortList.name, request=request),
            'project-acc-d1': reverse(api + ProjectAccountD1List.name, request=request),
            'project-acc-d2': reverse(api + ProjectAccountD2List.name, request=request),
            'wise-say': reverse(api + WiseSayList.name, request=request),
            # project
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
            'all-site': reverse(api + AllSiteList.name, request=request),
            'sites-total': reverse(api + TotalSiteArea.name, request=request),
            'site': reverse(api + 'site-list', request=request),
            'all-owner': reverse(api + AllOwnerList.name, request=request),
            'owners-total': reverse(api + TotalOwnerArea.name, request=request),
            'site-owner': reverse(api + 'siteowner-list', request=request),
            'site-relation': reverse(api + 'relation-list', request=request),
            'conts-total': reverse(api + TotalContractedArea.name, request=request),
            'site-contract': reverse(api + 'sitecontract-list', request=request),
            # cash
            'bank-code': reverse(api + BankCodeList.name, request=request),
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
            # 'over-due-rule': reverse(apiV1 + OverDueRuleList.name, request=request),
            # contract
            'order-group': reverse(api + 'order_group-list', request=request),
            'contract': reverse(api + 'contract-list', request=request),
            'contract-set': reverse(api + 'contract-set-list', request=request),
            'subs-sum': reverse(api + SubsSummaryList.name, request=request),
            'cont-sum': reverse(api + ContSummaryList.name, request=request),
            'contractor': reverse(api + 'contractor-list', request=request),
            'contractor-address': reverse(api + 'cont_address-list', request=request),
            'contractor-contact': reverse(api + 'contact-list', request=request),
            'contractor-release': reverse(api + 'release-list', request=request),
            # notice
            'sales-bill-issue': reverse(api + 'bill-list', request=request),
            # document
            'group': reverse(api + 'group-list', request=request),
            'board': reverse(api + 'board-list', request=request),
            'category': reverse(api + 'category-list', request=request),
            'suitcase': reverse(api + 'suitcase-list', request=request),
            'post': reverse(api + 'post-list', request=request),
            'image': reverse(api + 'image-list', request=request),
            'link': reverse(api + 'link-list', request=request),
            'file': reverse(api + 'file-list', request=request),
            'comment': reverse(api + 'comment-list', request=request),
            'tag': reverse(api + 'tag-list', request=request),
        })


app_name = 'apiV1'

list_view = {'get': 'list', 'post': 'create'}
detail_view = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}

urlpatterns = [
    # accounts
    path('', ApiIndex.as_view(), name=ApiIndex.name),
    path('user/', UserViewSets.as_view(list_view), name='user-list'),
    path('user/<int:pk>/', UserViewSets.as_view(detail_view), name='user-detail'),
    path('profile/', ProfileViewSets.as_view(list_view), name='profile-list'),
    path('profile/<int:pk>/', ProfileViewSets.as_view(detail_view), name='profile-detail'),
    path('todo/', TodoViewSets.as_view(list_view), name='todo-list'),
    path('todo/<int:pk>/', TodoViewSets.as_view(detail_view), name='todo-detail'),
    # company
    path('company/', CompanyViewSets.as_view(list_view), name='company-list'),
    path('company/<int:pk>/', CompanyViewSets.as_view(detail_view), name='company-detail'),
    path('logo/', LogoViewSets.as_view(list_view), name='logo-list'),
    path('logo/<int:pk>/', LogoViewSets.as_view(detail_view), name='logo-detail'),
    path('department/', DepartmentViewSets.as_view(list_view), name='depart-list'),
    path('department/<int:pk>/', DepartmentViewSets.as_view(detail_view), name='depart-detail'),
    path('position/', PositionViewSets.as_view(list_view), name='position-list'),
    path('position/<int:pk>/', PositionViewSets.as_view(detail_view), name='position-detail'),
    path('staff/', StaffViewSets.as_view(list_view), name='staff-list'),
    path('staff/<int:pk>/', StaffViewSets.as_view(detail_view), name='staff-detail'),
    # rebs
    path('schedule/', CalendarScheduleViewSet.as_view(list_view), name='schedule-list'),
    path('schedule/<int:pk>/', CalendarScheduleViewSet.as_view(detail_view), name='schedule-detail'),
    path('account-sort/', AccountSortList.as_view(), name=AccountSortList.name),
    path('account-depth1/', AccountSubD1List.as_view(), name=AccountSubD1List.name),
    path('account-depth2/', AccountSubD2List.as_view(), name=AccountSubD2List.name),
    path('account-depth3/', AccountSubD3List.as_view(), name=AccountSubD3List.name),
    path('project-acc-sort/', ProjectAccountSortList.as_view(), name=ProjectAccountSortList.name),
    path('project-account-depth1/', ProjectAccountD1List.as_view(), name=ProjectAccountD1List.name),
    path('project-account-depth2/', ProjectAccountD2List.as_view(), name=ProjectAccountD2List.name),
    path('wise-say/', WiseSayList.as_view(), name=WiseSayList.name),
    path('wise-say/<int:pk>/', WiseSayDetail.as_view(), name=WiseSayDetail.name),
    # project
    path('project/', ProjectViewSets.as_view(list_view), name='project-list'),
    path('project/<int:pk>/', ProjectViewSets.as_view(detail_view), name='project-detail'),
    path('type/', UnitTypeViewSets.as_view(list_view), name='unittype-list'),
    path('type/<int:pk>/', UnitTypeViewSets.as_view(detail_view), name='unittype-detail'),
    path('floor/', UnitFloorTypeViewSets.as_view(list_view), name='floortype-list'),
    path('floor/<int:pk>/', UnitFloorTypeViewSets.as_view(detail_view), name='floortype-detail'),
    path('key-unit/', KeyUnitViewSets.as_view(list_view), name='key_unit-list'),
    path('key-unit/<int:pk>/', KeyUnitViewSets.as_view(detail_view), name='key_unit-detail'),
    path('bldg/', BuildingUnitViewSets.as_view(list_view), name='bldg-list'),
    path('bldg/<int:pk>/', BuildingUnitViewSets.as_view(detail_view), name='bldg-detail'),
    path('house-unit/', HouseUnitList.as_view(), name=HouseUnitList.name),
    path('house-unit/<int:pk>/', HouseUnitDetail.as_view(), name=HouseUnitDetail.name),
    path('available-house-unit/', AvailableHouseUnitList.as_view(), name=AvailableHouseUnitList.name),
    path('all-house-unit/', AllHouseUnitList.as_view(), name=AllHouseUnitList.name),
    path('budget/', ProjectBudgetList.as_view(), name=ProjectBudgetList.name),
    # path('budget/<int:pk>/', ProjectBudgetDetail.as_view(), name=ProjectBudgetDetail.name),
    path('exec-amount/', ExecAmountToBudgetList.as_view(), name=ExecAmountToBudgetList.name),
    path('site/', SiteViewSets.as_view(list_view), name='site-list'),
    path('all-site/', AllSiteList.as_view(), name=AllSiteList.name),
    path('sites-total/', TotalSiteArea.as_view(), name=TotalSiteArea.name),
    path('site/<int:pk>/', SiteViewSets.as_view(detail_view), name='site-detail'),
    path('all-owner/', AllOwnerList.as_view(), name=AllOwnerList.name),
    path('owners-total/', TotalOwnerArea.as_view(), name=TotalOwnerArea.name),
    path('site-owner/', SiteOwnerViewSets.as_view(list_view), name='siteowner-list'),
    path('site-owner/<int:pk>/', SiteOwnerViewSets.as_view(detail_view), name='siteowner-detail'),
    path('site-relation/', SiteRelationViewSets.as_view(list_view), name='relation-list'),
    path('site-relation/<int:pk>/', SiteRelationViewSets.as_view(detail_view), name='relation-detail'),
    path('conts-total/', TotalContractedArea.as_view(), name=TotalContractedArea.name),
    path('site-contract/', SiteContractViewSets.as_view(list_view), name='sitecontract-list'),
    path('site-contract/<int:pk>/', SiteContractViewSets.as_view(detail_view), name='sitecontract-detail'),
    # cash
    path('bank-code/', BankCodeList.as_view(), name=BankCodeList.name),
    path('bank-code/<int:pk>/', BankCodeDetail.as_view(), name=BankCodeDetail.name),
    path('company-bank-account/', ComBankAccountViewSets.as_view(list_view), name='com_bank-list'),
    path('company-bank-account/<int:pk>/', ComBankAccountViewSets.as_view(detail_view), name='com_bank-detail'),
    path('balance-by-acc/', BalanceByAccountList.as_view(), name=BalanceByAccountList.name),
    path('cashbook/', CashBookList.as_view(), name=CashBookList.name),
    path('cashbook/<int:pk>/', CashBookDetail.as_view(), name=CashBookDetail.name),
    path('date-cashbook/', DateCashBookList.as_view(), name=DateCashBookList.name),
    path('project-bank-account/', ProjectBankAccountList.as_view(), name=ProjectBankAccountList.name),
    path('project-bank-account/<int:pk>/', ProjectBankAccountDetail.as_view(), name=ProjectBankAccountDetail.name),
    path('pr-balance-by-acc/', PrBalanceByAccountList.as_view(), name=PrBalanceByAccountList.name),
    path('pr-date-cashbook/', ProjectDateCashBookList.as_view(), name=ProjectDateCashBookList.name),
    path('project-cashbook/', ProjectCashBookList.as_view(), name=ProjectCashBookList.name),
    path('project-cashbook/<int:pk>/', ProjectCashBookDetail.as_view(), name=ProjectCashBookDetail.name),
    path('project-imprest/', ProjectImprestList.as_view(), name=ProjectImprestList.name),
    path('payment/', PaymentList.as_view(), name=PaymentList.name),
    path('all-payment/', AllPaymentList.as_view(), name=AllPaymentList.name),

    path('payment-sum/', PaymentSummary.as_view(), name=PaymentSummary.name),
    path('contract-num/', NumContractByType.as_view(), name=NumContractByType.name),
    path('price/', SalesPriceList.as_view(), name=SalesPriceList.name),
    path('price/<int:pk>/', SalesPriceDetail.as_view(), name=SalesPriceDetail.name),
    path('pay-order/', InstallmentOrderList.as_view(), name=InstallmentOrderList.name),
    path('pay-order/<int:pk>/', InstallmentOrderDetail.as_view(), name=InstallmentOrderDetail.name),
    path('down-payment/', DownPaymentList.as_view(), name=DownPaymentList.name),
    path('down-payment/<int:pk>/', DownPaymentDetail.as_view(), name=DownPaymentDetail.name),
    # path('over-due-rule/', OverDueRuleList.as_view(), name=OverDueRuleList.name),
    # path('over-due-rule/<int:pk>/', OverDueRuleDetail.as_view(), name=OverDueRuleDetail.name),
    # contract
    path('order-group/', OrderGroupViewSets.as_view(list_view), name='order_group-list'),
    path('order-group/<int:pk>/', OrderGroupViewSets.as_view(detail_view), name='order_group-detail'),
    path('contract/', ContractViewSets.as_view(list_view), name='contract-list'),
    path('contract/<int:pk>/', ContractViewSets.as_view(detail_view), name='contract-detail'),
    path('contract-set/', ContractSetViewSets.as_view(list_view), name='contract-set-list'),
    path('contract-set/<int:pk>/', ContractSetViewSets.as_view(detail_view), name='contract-set-detail'),
    path('subs-sum/', SubsSummaryList.as_view(), name=SubsSummaryList.name),
    path('cont-sum/', ContSummaryList.as_view(), name=ContSummaryList.name),

    path('contractor/', ContractorViewSets.as_view(list_view), name='contractor-list'),
    path('contractor/<int:pk>/', ContractorViewSets.as_view(detail_view), name='contractor-detail'),
    path('contractor-address/', ContAddressViewSets.as_view(list_view), name='cont_address-list'),
    path('contractor-address/<int:pk>/', ContAddressViewSets.as_view(detail_view), name='cont_address-detail'),
    path('contractor-contact/', ContContactViewSets.as_view(list_view), name='contact-list'),
    path('contractor-contact/<int:pk>/', ContContactViewSets.as_view(detail_view), name='contact-detail'),
    path('contractor-release/', ContReleaseViewSets.as_view(list_view), name='release-list'),
    path('contractor-release/<int:pk>/', ContReleaseViewSets.as_view(detail_view), name='release-detail'),
    # notice
    path('sales-bill-issue/', BillIssueViewSets.as_view(list_view), name='bill-list'),
    path('sales-bill-issue/<int:pk>/', BillIssueViewSets.as_view(detail_view), name='bill-detail'),
    # document
    path('group/', GroupViewSets.as_view(list_view), name='group-list'),
    path('group/<int:pk>/', GroupViewSets.as_view(detail_view), name='group-detail'),
    path('board/', BoardViewSets.as_view(list_view), name='board-list'),
    path('board/<int:pk>/', BoardViewSets.as_view(detail_view), name='board-detail'),
    path('category/', CategoryViewSets.as_view(list_view), name='category-list'),
    path('category/<int:pk>/', CategoryViewSets.as_view(detail_view), name='category-detail'),
    path('suitcase/', LawSuitCaseViewSets.as_view(list_view), name='suitcase-list'),
    path('suitcase/<int:pk>/', LawSuitCaseViewSets.as_view(detail_view), name='suitcase-detail'),
    path('post/', PostViewSets.as_view(list_view), name='post-list'),
    path('post/<int:pk>/', PostViewSets.as_view(detail_view), name='post-detail'),
    path('image/', ImageViewSets.as_view(list_view), name='image-list'),
    path('image/<int:pk>/', ImageViewSets.as_view(detail_view), name='image-detail'),
    path('link/', LinkViewSets.as_view(list_view), name='link-list'),
    path('link/<int:pk>/', LinkViewSets.as_view(detail_view), name='link-detail'),
    path('file/', FileViewSets.as_view(list_view), name='file-list'),
    path('file/<int:pk>/', FileViewSets.as_view(detail_view), name='file-detail'),
    path('comment/', CommentViewSets.as_view(list_view), name='comment-list'),
    path('comment/<int:pk>/', CommentViewSets.as_view(detail_view), name='comment-detail'),
    path('tag/', TagViewSets.as_view(list_view), name='tag-list'),
    path('tag/<int:pk>/', TagViewSets.as_view(detail_view), name='tag-detail'),

]
