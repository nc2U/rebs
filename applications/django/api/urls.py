"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import *

app_name = 'api'

urlpatterns = [
    path('', ApiIndex.as_view(), name=ApiIndex.name),
    path('user/', UserList.as_view(), name=UserList.name),
    path('user/<int:pk>/', UserDetail.as_view(), name=UserDetail.name),
    path('profile/', ProfileList.as_view(), name=ProfileList.name),
    path('profile/<int:pk>/', ProfileDetail.as_view(), name=ProfileDetail.name),
    path('todo/', TodoList.as_view(), name=TodoList.name),
    path('todo/<int:pk>/', TodoDetail.as_view(), name=TodoDetail.name),
    path('staff/', StaffList.as_view(), name=StaffList.name),
    path('staff/<int:pk>/', StaffDetail.as_view(), name=StaffDetail.name),
    path('company/', CompanyList.as_view(), name=CompanyList.name),
    path('company/<int:pk>/', CompanyDetail.as_view(), name=CompanyDetail.name),
    path('department/', DepartmentList.as_view(), name=DepartmentList.name),
    path('department/<int:pk>/', DepartmentDetail.as_view(), name=DepartmentDetail.name),
    path('position/', PositionList.as_view(), name=PositionList.name),
    path('position/<int:pk>/', PositionDetail.as_view(), name=PositionDetail.name),

    path('account-sort/', AccountSortList.as_view(), name=AccountSortList.name),
    path('account-depth1/', AccountSubD1List.as_view(), name=AccountSubD1List.name),
    path('account-depth2/', AccountSubD2List.as_view(), name=AccountSubD2List.name),
    path('account-depth3/', AccountSubD3List.as_view(), name=AccountSubD3List.name),
    path('project-acc-sort/', ProjectAccountSortList.as_view(), name=ProjectAccountSortList.name),
    path('project-account-depth1/', ProjectAccountD1List.as_view(), name=ProjectAccountD1List.name),
    path('project-account-depth2/', ProjectAccountD2List.as_view(), name=ProjectAccountD2List.name),

    path('project/', ProjectList.as_view(), name=ProjectList.name),
    path('project/<int:pk>/', ProjectDetail.as_view(), name=ProjectDetail.name),
    path('type/', UnitTypeList.as_view(), name=UnitTypeList.name),
    path('type/<int:pk>/', UnitTypeDetail.as_view(), name=UnitTypeDetail.name),
    path('floor/', UnitFloorTypeList.as_view(), name=UnitFloorTypeList.name),
    path('floor/<int:pk>/', UnitFloorTypeDetail.as_view(), name=UnitFloorTypeDetail.name),
    path('key-unit/', KeyUnitList.as_view(), name=KeyUnitList.name),
    path('key-unit/<int:pk>/', KeyUnitDetail.as_view(), name=KeyUnitDetail.name),
    path('bldg/', BuildingUnitList.as_view(), name=BuildingUnitList.name),
    path('bldg/<int:pk>/', BuildingUnitDetail.as_view(), name=BuildingUnitDetail.name),
    path('house-unit/', HouseUnitList.as_view(), name=HouseUnitList.name),
    path('house-unit/<int:pk>/', HouseUnitDetail.as_view(), name=HouseUnitDetail.name),
    path('available-house-unit/', AvailableHouseUnitList.as_view(), name=AvailableHouseUnitList.name),
    path('all-house-unit/', AllHouseUnitList.as_view(), name=AllHouseUnitList.name),
    path('budget/', ProjectBudgetList.as_view(), name=ProjectBudgetList.name),
    # path('budget/<int:pk>/', ProjectBudgetDetail.as_view(), name=ProjectBudgetDetail.name),
    path('exec-amount/', ExecAmountToBudgetList.as_view(), name=ExecAmountToBudgetList.name),
    # path('site/', SiteList.as_view(), name=SiteList.name),
    # path('site/<int:pk>/', SiteDetail.as_view(), name=SiteDetail.name),
    # path('site-owner/', SiteOwnerList.as_view(), name=SiteOwnerList.name),
    # path('site-owner/<int:pk>/', SiteOwnerDetail.as_view(), name=SiteOwnerDetail.name),
    # path('site-relation/', RelationList.as_view(), name=RelationList.name),
    # path('site-relation/<int:pk>/', RelationDetail.as_view(), name=RelationDetail.name),
    # path('site-contract/', SiteContractList.as_view(), name=SiteContractList.name),
    # path('site-contract/<int:pk>/', SiteContractDetail.as_view(), name=SiteContractDetail.name),

    # path('bank-code/', BankCodeList.as_view(), name=BankCodeList.name),
    # path('bank-code/<int:pk>/', BankCodeDetail.as_view(), name=BankCodeDetail.name),
    path('company-bank-account/', ComBankAccountList.as_view(), name=ComBankAccountList.name),
    path('company-bank-account/<int:pk>/', ComBankAccountDetail.as_view(), name=ComBankAccountDetail.name),
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
    path('order-group/', OrderGroupList.as_view(), name=OrderGroupList.name),
    path('order-group/<int:pk>/', OrderGroupDetail.as_view(), name=OrderGroupDetail.name),
    path('contract/', ContractList.as_view(), name=ContractList.name),
    path('contract/<int:pk>/', ContractDetail.as_view(), name=ContractDetail.name),
    path('contract-custom-list/', ContractCustomList.as_view(), name=ContractCustomList.name),
    path('contract-custom-list/<int:pk>/', ContractCustomDetail.as_view(), name=ContractCustomDetail.name),
    path('subs-sum/', SubsSummaryList.as_view(), name=SubsSummaryList.name),
    path('cont-sum/', ContSummaryList.as_view(), name=ContSummaryList.name),

    path('contractor/', ContractorList.as_view(), name=ContractorList.name),
    path('contractor/<int:pk>/', ContractorDetail.as_view(), name=ContractorDetail.name),
    path('contractor-address/', ContAddressList.as_view(), name=ContAddressList.name),
    path('contractor-address/<int:pk>/', ContAddressDetail.as_view(), name=ContAddressDetail.name),
    path('contractor-contact/', ContContactList.as_view(), name=ContContactList.name),
    path('contractor-contact/<int:pk>/', ContContactDetail.as_view(), name=ContContactDetail.name),
    path('contractor-release/', ContReleaseList.as_view(), name=ContReleaseList.name),
    path('contractor-release/<int:pk>/', ContReleaseDetail.as_view(), name=ContReleaseDetail.name),
    # path('sales-bill-issue/', BillIssueList.as_view(), name=BillIssueList.name),
    # path('sales-bill-issue/<int:pk>/', BillIssueDetail.as_view(), name=BillIssueDetail.name),
    # path('group/', GroupList.as_view(), name=GroupList.name),
    # path('group/<int:pk>/', GroupDetail.as_view(), name=GroupDetail.name),
    # path('board/', BoardList.as_view(), name=BoardList.name),
    # path('board/<int:pk>/', BoardDetail.as_view(), name=BoardDetail.name),
    # path('category/', CategoryList.as_view(), name=CategoryList.name),
    # path('category/<int:pk>/', CategoryDetail.as_view(), name=CategoryDetail.name),
    # path('suitcase/', LawSuitCaseList.as_view(), name=LawSuitCaseList.name),
    # path('suitcase/<int:pk>/', LawSuitCaseDetail.as_view(), name=LawSuitCaseDetail.name),
    # path('post/', PostList.as_view(), name=PostList.name),
    # path('post/<int:pk>/', PostDetail.as_view(), name=PostDetail.name),
    # path('image/', ImageList.as_view(), name=ImageList.name),
    # path('image/<int:pk>/', ImageDetail.as_view(), name=ImageDetail.name),
    # path('link/', LinkList.as_view(), name=LinkList.name),
    # path('link/<int:pk>/', LinkDetail.as_view(), name=LinkDetail.name),
    # path('file/', FileList.as_view(), name=FileList.name),
    # path('file/<int:pk>/', FileDetail.as_view(), name=FileDetail.name),
    # path('comment/', CommentList.as_view(), name=CommentList.name),
    # path('comment/<int:pk>/', CommentDetail.as_view(), name=CommentDetail.name),
    # path('tag/', TagList.as_view(), name=TagList.name),
    # path('tag/<int:pk>/', TagDetail.as_view(), name=TagDetail.name),
    path('wise-say/', WiseSayList.as_view(), name=WiseSayList.name),
    path('wise-say/<int:pk>/', WiseSayDetail.as_view(), name=WiseSayDetail.name),
]
