from rest_framework.routers import DefaultRouter

from .views import accounts
from .views import company
from .views import rebs
from .views import project
from .views import cash
from .views import contract
from .views import notice
from .views import document

app_name = 'apiV1'

router = DefaultRouter()
# accounts
router.register(r'user', accounts.UserViewSet)
router.register(r'profile', accounts.ProfileViewSet)
router.register(r'todo', accounts.TodoViewSet)
# company
router.register(r'company', company.CompanyViewSet)
router.register(r'logo', company.LogoViewSet)
router.register(r'department', company.DepartmentViewSet)
router.register(r'position', company.PositionViewSet)
router.register(r'staff', company.StaffViewSet)
# rebs
router.register(r'schedule', rebs.CalendarScheduleViewSet)
router.register(r'account-sort', rebs.AccountSortViewSet)  # only list
router.register(r'account-depth1', rebs.AccountSubD1ViewSet)  # only list
router.register(r'account-depth2', rebs.AccountSubD2ViewSet)  # only list
router.register(r'account-depth3', rebs.AccountSubD3ViewSet)  # only list
router.register(r'project-acc-sort', rebs.ProjectAccountSortViewSet)  # only list
router.register(r'project-account-depth1', rebs.ProjectAccountD1ViewSet)  # only list
router.register(r'project-account-depth2', rebs.ProjectAccountD2ViewSet)  # only list
router.register(r'wise-say', rebs.WiseSayViewSet)
# project
router.register(r'project', project.ProjectViewSet)
router.register(r'type', project.UnitTypeViewSet)
router.register(r'floor', project.UnitFloorTypeViewSet)
router.register(r'key-unit', project.KeyUnitViewSet)
router.register(r'bldg', project.BuildingUnitViewSet)
router.register(r'house-unit', project.HouseUnitViewSet)
router.register(r'available-house-unit', project.AvailableHouseUnitViewSet)  # only list
router.register(r'all-house-unit', project.AllHouseUnitViewSet)  # only list
router.register(r'budget', project.ProjectBudgetViewSet)  # only list
router.register(r'exec-amount', project.ExecAmountToBudgetViewSet, basename='exec-amount')  # only list
router.register(r'site', project.SiteViewSet)
router.register(r'all-site', project.AllSiteViewSet)  # only list
router.register(r'sites-total', project.TotalSiteAreaViewSet, basename='sites-total')  # only list
router.register(r'site-owner', project.SiteOwnerViewSet)
router.register(r'all-owner', project.AllOwnerViewSet)  # only list
router.register(r'owners-total', project.TotalOwnerAreaViewSet, basename='owners-total')  # only list
router.register(r'site-relation', project.SiteRelationViewSet)
router.register(r'site-contract', project.SiteContractViewSet)
router.register(r'conts-total', project.TotalContractedAreaViewSet, basename='conts-total')  # only list
# cash
router.register(r'bank-code', cash.BankCodeViewSet)
router.register(r'company-bank-account', cash.ComBankAccountViewSet)
router.register(r'balance-by-acc', cash.BalanceByAccountViewSet, basename='balance-by-acc')  # only list
router.register(r'cashbook', cash.CashBookViewSet)
router.register(r'date-cashbook', cash.DateCashBookViewSet)  # only list
router.register(r'project-bank-account', cash.ProjectBankAccountViewSet)
router.register(r'pr-balance-by-acc', cash.PrBalanceByAccountViewSet, basename='pr-balance-by-acc')  # only list
router.register(r'project-cashbook', cash.ProjectCashBookViewSet)
router.register(r'pr-date-cashbook', cash.ProjectDateCashBookViewSet)  # only list
router.register(r'project-imprest', cash.ProjectImprestViewSet)  # only list
router.register(r'payment', cash.PaymentViewSet)  # only list
router.register(r'all-payment', cash.AllPaymentViewSet)  # only list
router.register(r'payment-sum', cash.PaymentSummaryViewSet, basename='payment-sum')  # only list
router.register(r'contract-num', cash.NumContractByTypeViewSet, basename='contract-num')  # only list
router.register(r'price', cash.SalesPriceViewSet)
router.register(r'pay-order', cash.InstallmentOrderViewSet)
router.register(r'down-payment', cash.DownPaymentViewSet)
# contract
router.register(r'order-group', contract.OrderGroupViewSet)
router.register(r'contract', contract.ContractViewSet)
router.register(r'contract-set', contract.ContractSetViewSet)
router.register(r'subs-sum', contract.SubsSummaryViewSet, basename='subs-sum')  # only list
router.register(r'cont-sum', contract.ContSummaryViewSet, basename='cont-sum')  # only list
router.register(r'contractor', contract.ContractorViewSet)
router.register(r'contractor-address', contract.ContAddressViewSet)
router.register(r'contractor-contact', contract.ContContactViewSet)
router.register(r'contractor-release', contract.ContReleaseViewSet)
# notice
router.register(r'sales-bill-issue', notice.BillIssueViewSet)
# document
router.register(r'group', document.GroupViewSet)
router.register(r'board', document.BoardViewSet)
router.register(r'category', document.CategoryViewSet)
router.register(r'suitcase', document.LawSuitCaseViewSet)
router.register(r'post', document.PostViewSet)
router.register(r'link', document.LinkViewSet)
router.register(r'image', document.ImageViewSet)
router.register(r'file', document.FileViewSet)
router.register(r'comment', document.CommentViewSet)
router.register(r'tag', document.TagViewSet)

urlpatterns = router.urls

# list_view = {'get': 'list', 'post': 'create'}
# detail_view = {
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# }

# urlpatterns = [
#     # accounts
#     # path('user/', UserViewSet.as_view(list_view), name='user-list'),
#     # path('user/<int:pk>/', UserViewSet.as_view(detail_view), name='user-detail'),
#     # path('profile/', ProfileViewSet.as_view(list_view), name='profile-list'),
#     # path('profile/<int:pk>/', ProfileViewSet.as_view(detail_view), name='profile-detail'),
#     # path('todo/', TodoViewSet.as_view(list_view), name='todo-list'),
#     # path('todo/<int:pk>/', TodoViewSet.as_view(detail_view), name='todo-detail'),
#
#     # company
#     # path('company/', CompanyViewSet.as_view(list_view), name='company-list'),
#     # path('company/<int:pk>/', CompanyViewSet.as_view(detail_view), name='company-detail'),
#     # path('logo/', LogoViewSet.as_view(list_view), name='logo-list'),
#     # path('logo/<int:pk>/', LogoViewSet.as_view(detail_view), name='logo-detail'),
#     # path('department/', DepartmentViewSet.as_view(list_view), name='depart-list'),
#     # path('department/<int:pk>/', DepartmentViewSet.as_view(detail_view), name='depart-detail'),
#     # path('position/', PositionViewSet.as_view(list_view), name='position-list'),
#     # path('position/<int:pk>/', PositionViewSet.as_view(detail_view), name='position-detail'),
#     # path('staff/', StaffViewSet.as_view(list_view), name='staff-list'),
#     # path('staff/<int:pk>/', StaffViewSet.as_view(detail_view), name='staff-detail'),
#
#     # rebs
#     # path('schedule/', CalendarScheduleViewSet.as_view(list_view), name='schedule-list'),
#     # path('schedule/<int:pk>/', CalendarScheduleViewSet.as_view(detail_view), name='schedule-detail'),
#     # path('account-sort/', AccountSortViewSet.as_view(list_view), name='acc_sort-list'),
#     # path('account-depth1/', AccountSubD1ViewSet.as_view(list_view), name='acc_d1-list'),
#     # path('account-depth2/', AccountSubD2ViewSet.as_view(list_view), name='acc_d2-list'),
#     # path('account-depth3/', AccountSubD3ViewSet.as_view(list_view), name='acc_d3-list'),
#     # path('project-acc-sort/', ProjectAccountSortViewSet.as_view(list_view), name='pro-acc_sort-list'),
#     # path('project-account-depth1/', ProjectAccountD1ViewSet.as_view(list_view), name='project_acc_d1-list'),
#     # path('project-account-depth2/', ProjectAccountD2ViewSet.as_view(list_view), name='project_acc_d2-list'),
#     # path('wise-say/', WiseSayViewSet.as_view(list_view), name='wise-say-list'),
#     # path('wise-say/<int:pk>/', WiseSayViewSet.as_view(detail_view), name='wise-say-detail'),
#
#     # project
#     # path('project/', ProjectViewSet.as_view(list_view), name='project-list'),
#     # path('project/<int:pk>/', ProjectViewSet.as_view(detail_view), name='project-detail'),
#     # path('type/', UnitTypeViewSet.as_view(list_view), name='unittype-list'),
#     # path('type/<int:pk>/', UnitTypeViewSet.as_view(detail_view), name='unittype-detail'),
#     # path('floor/', UnitFloorTypeViewSet.as_view(list_view), name='floortype-list'),
#     # path('floor/<int:pk>/', UnitFloorTypeViewSet.as_view(detail_view), name='floortype-detail'),
#     # path('key-unit/', KeyUnitViewSet.as_view(list_view), name='key_unit-list'),
#     # path('key-unit/<int:pk>/', KeyUnitViewSet.as_view(detail_view), name='key_unit-detail'),
#     # path('bldg/', BuildingUnitViewSet.as_view(list_view), name='bldg-list'),
#     # path('bldg/<int:pk>/', BuildingUnitViewSet.as_view(detail_view), name='bldg-detail'),
#     # path('house-unit/', HouseUnitViewSet.as_view(list_view), name='unit-list'),
#     # path('house-unit/<int:pk>/', HouseUnitViewSet.as_view(detail_view), name='unit-detail'),
#     # path('available-house-unit/', AvailableHouseUnitViewSet.as_view(list_view), name='available-unit-list'),
#     # path('all-house-unit/', AllHouseUnitViewSet.as_view(list_view), name='all-unit-list'),
#     # path('budget/', ProjectBudgetViewSet.as_view(list_view), name='projectbudget-list'),
#     # path('budget/<int:pk>/', ProjectBudgetDetail.as_view(), name=ProjectBudgetDetail.name),
#     # path('exec-amount/', ExecAmountToBudgetViewSet.as_view(list_view), name='execution-amount'),
#     # path('site/', SiteViewSet.as_view(list_view), name='site-list'),
#     # path('site/<int:pk>/', SiteViewSet.as_view(detail_view), name='site-detail'),
#     # path('all-site/', AllSiteViewSet.as_view(list_view), name='all-site'),
#     # path('sites-total/', TotalSiteAreaViewSet.as_view(list_view), name='sites-total'),
#     # path('site-owner/', SiteOwnerViewSet.as_view(list_view), name='siteowner-list'),
#     # path('site-owner/<int:pk>/', SiteOwnerViewSet.as_view(detail_view), name='siteowner-detail'),
#     # path('all-owner/', AllOwnerViewSet.as_view(list_view), name='all-owner'),
#     # path('owners-total/', TotalOwnerAreaViewSet.as_view(list_view), name='owners-total'),
#     # path('site-relation/', SiteRelationViewSet.as_view(list_view), name='relation-list'),
#     # path('site-relation/<int:pk>/', SiteRelationViewSet.as_view(detail_view), name='relation-detail'),
#     # path('site-contract/', SiteContractViewSet.as_view(list_view), name='sitecontract-list'),
#     # path('site-contract/<int:pk>/', SiteContractViewSet.as_view(detail_view), name='sitecontract-detail'),
#     # path('conts-total/', TotalContractedAreaViewSet.as_view(list_view), name='conts-total'),
#
#     # cash
#     # path('bank-code/', BankCodeViewSet.as_view(list_view), name='bankcode-list'),
#     # path('bank-code/<int:pk>/', BankCodeViewSet.as_view(detail_view), name='bankcode-detail'),
#     # path('company-bank-account/', ComBankAccountViewSet.as_view(list_view), name='com_bank-list'),
#     # path('company-bank-account/<int:pk>/', ComBankAccountViewSet.as_view(detail_view), name='com_bank-detail'),
#     # path('balance-by-acc/', BalanceByAccountViewSet.as_view(list_view), name='balance-by-acc'),
#     # path('cashbook/', CashBookViewSet.as_view(list_view), name='cashbook-list'),
#     # path('cashbook/<int:pk>/', CashBookViewSet.as_view(detail_view), name='cashbook-detail'),
#     # path('date-cashbook/', DateCashBookViewSet.as_view(list_view), name='date-cashbook'),
#     # path('project-bank-account/', ProjectBankAccountViewSet.as_view(list_view), name='project_bank-list'),
#     # path('project-bank-account/<int:pk>/', ProjectBankAccountViewSet.as_view(detail_view), name='project_bank-detail'),
#     # path('pr-balance-by-acc/', PrBalanceByAccountViewSet.as_view(list_view), name='pr-balance-by-acc'),
#     # path('project-cashbook/', ProjectCashBookViewSet.as_view(list_view), name='project_cashbook-list'),
#     # path('project-cashbook/<int:pk>/', ProjectCashBookViewSet.as_view(detail_view), name='project_cashbook-detail'),
#     # path('pr-date-cashbook/', ProjectDateCashBookViewSet.as_view(list_view), name='pr-date-cashbook'),
#     # path('project-imprest/', ProjectImprestViewSet.as_view(list_view), name='project-imprest-list'),
#     # path('payment/', PaymentViewSet.as_view(list_view), name='payment-list'),
#     # path('all-payment/', AllPaymentViewSet.as_view(list_view), name='all-payment-list'),
#     # path('payment-sum/', PaymentSummaryViewSet.as_view(list_view), name='payment-sum'),
#     # path('contract-num/', NumContractByTypeViewSet.as_view(list_view), name='cont-count'),
#     # path('price/', SalesPriceViewSet.as_view(list_view), name='price-list'),
#     # path('price/<int:pk>/', SalesPriceViewSet.as_view(detail_view), name='price-detail'),
#     # path('pay-order/', InstallmentOrderViewSet.as_view(list_view), name='install_order-list'),
#     # path('pay-order/<int:pk>/', InstallmentOrderViewSet.as_view(detail_view), name='install_order-detail'),
#     # path('down-payment/', DownPaymentViewSet.as_view(list_view), name='downpay-list'),
#     # path('down-payment/<int:pk>/', DownPaymentViewSet.as_view(detail_view), name='downpay-detail'),
#     # path('over-due-rule/', OverDueRuleList.as_view(), name=OverDueRuleList.name),
#     # path('over-due-rule/<int:pk>/', OverDueRuleDetail.as_view(), name=OverDueRuleDetail.name),
#
#     # contract
#     # path('order-group/', OrderGroupViewSet.as_view(list_view), name='order_group-list'),
#     # path('order-group/<int:pk>/', OrderGroupViewSet.as_view(detail_view), name='order_group-detail'),
#     # path('contract/', ContractViewSet.as_view(list_view), name='contract-list'),
#     # path('contract/<int:pk>/', ContractViewSet.as_view(detail_view), name='contract-detail'),
#     # path('contract-set/', ContractSetViewSet.as_view(list_view), name='contract-set-list'),
#     # path('contract-set/<int:pk>/', ContractSetViewSet.as_view(detail_view), name='contract-set-detail'),
#     # path('subs-sum/', SubsSummaryViewSet.as_view(list_view), name='subs-summary'),
#     # path('cont-sum/', ContSummaryViewSet.as_view(list_view), name='cont-summary'),
#     # path('contractor/', ContractorViewSet.as_view(list_view), name='contractor-list'),
#     # path('contractor/<int:pk>/', ContractorViewSet.as_view(detail_view), name='contractor-detail'),
#     # path('contractor-address/', ContAddressViewSet.as_view(list_view), name='cont_address-list'),
#     # path('contractor-address/<int:pk>/', ContAddressViewSet.as_view(detail_view), name='cont_address-detail'),
#     # path('contractor-contact/', ContContactViewSet.as_view(list_view), name='contact-list'),
#     # path('contractor-contact/<int:pk>/', ContContactViewSet.as_view(detail_view), name='contact-detail'),
#     # path('contractor-release/', ContReleaseViewSet.as_view(list_view), name='release-list'),
#     # path('contractor-release/<int:pk>/', ContReleaseViewSet.as_view(detail_view), name='release-detail'),
#     # notice
#     # path('sales-bill-issue/', BillIssueViewSet.as_view(list_view), name='bill-list'),
#     # path('sales-bill-issue/<int:pk>/', BillIssueViewSet.as_view(detail_view), name='bill-detail'),
#     # document
#     # path('group/', GroupViewSet.as_view(list_view), name='group-list'),
#     # path('group/<int:pk>/', GroupViewSet.as_view(detail_view), name='group-detail'),
#     # path('board/', BoardViewSet.as_view(list_view), name='board-list'),
#     # path('board/<int:pk>/', BoardViewSet.as_view(detail_view), name='board-detail'),
#     # path('category/', CategoryViewSet.as_view(list_view), name='category-list'),
#     # path('category/<int:pk>/', CategoryViewSet.as_view(detail_view), name='category-detail'),
#     # path('suitcase/', LawSuitCaseViewSet.as_view(list_view), name='suitcase-list'),
#     # path('suitcase/<int:pk>/', LawSuitCaseViewSet.as_view(detail_view), name='suitcase-detail'),
#     # path('post/', PostViewSet.as_view(list_view), name='post-list'),
#     # path('post/<int:pk>/', PostViewSet.as_view(detail_view), name='post-detail'),
#     # path('like/', LikeViewSet.as_view(list_view), name='like-list'),
#     # path('like/<int:pk>/', LikeViewSet.as_view(detail_view), name='like-detail'),
#     # path('dislike/', DisLikeViewSet.as_view(list_view), name='dislike-list'),
#     # path('dislike/<int:pk>/', DisLikeViewSet.as_view(detail_view), name='dislike-detail'),
#     # path('link/', LinkViewSet.as_view(list_view), name='link-list'),
#     # path('link/<int:pk>/', LinkViewSet.as_view(detail_view), name='link-detail'),
#     # path('image/', ImageViewSet.as_view(list_view), name='image-list'),
#     # path('image/<int:pk>/', ImageViewSet.as_view(detail_view), name='image-detail'),
#     # path('file/', FileViewSet.as_view(list_view), name='file-list'),
#     # path('file/<int:pk>/', FileViewSet.as_view(detail_view), name='file-detail'),
#     # path('comment/', CommentViewSet.as_view(list_view), name='comment-list'),
#     # path('comment/<int:pk>/', CommentViewSet.as_view(detail_view), name='comment-detail'),
#     # path('tag/', TagViewSet.as_view(list_view), name='tag-list'),
#     # path('tag/<int:pk>/', TagViewSet.as_view(detail_view), name='tag-detail'),
# ]


# class ApiIndex(generics.GenericAPIView):
#     name = 'apiV1-index'
#     permission_classes = (permissions.AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         api = 'apiV1:'
#         return Response({
#             # accounts
#             'user': reverse(api + 'user-list', request=request),
#             'profile': reverse(api + 'profile-list', request=request),
#             'todo': reverse(api + 'todo-list', request=request),
#             # company
#             'company': reverse(api + 'company-list', request=request),
#             'logo': reverse(api + 'logo-list', request=request),
#             'department': reverse(api + 'depart-list', request=request),
#             'position': reverse(api + 'position-list', request=request),
#             'staff': reverse(api + 'staff-list', request=request),
#             # rebs
#             'schedule': reverse(api + 'schedule-list', request=request),
#             'account-sort': reverse(api + 'acc_sort-list', request=request),
#             'account-depth1': reverse(api + 'acc_d1-list', request=request),
#             'account-depth2': reverse(api + 'acc_d2-list', request=request),
#             'account-depth3': reverse(api + 'acc_d3-list', request=request),
#             'project-acc-sort': reverse(api + 'pro-acc_sort-list', request=request),
#             'project-acc-d1': reverse(api + 'project_acc_d1-list', request=request),
#             'project-acc-d2': reverse(api + 'project_acc_d2-list', request=request),
#             'wise-say': reverse(api + 'wise-say-list', request=request),
#             # project
#             'project': reverse(api + 'project-list', request=request),
#             'type': reverse(api + 'unittype-list', request=request),
#             'floor': reverse(api + 'floortype-list', request=request),
#             'key-unit': reverse(api + 'key_unit-list', request=request),
#             'bldg-unit': reverse(api + 'bldg-list', request=request),
#             'house-unit': reverse(api + 'unit-list', request=request),
#             'available-house-unit': reverse(api + 'available-unit-list', request=request),
#             'all-house-unit': reverse(api + 'all-unit-list', request=request),
#             'budget': reverse(api + 'projectbudget-list', request=request),
#             'exec-amount-budget': reverse(api + 'execution-amount', request=request),
#             'all-site': reverse(api + 'all-site', request=request),
#             'sites-total': reverse(api + 'sites-total', request=request),
#             'site': reverse(api + 'site-list', request=request),
#             'all-owner': reverse(api + 'all-owner', request=request),
#             'owners-total': reverse(api + 'owners-total', request=request),
#             'site-owner': reverse(api + 'siteowner-list', request=request),
#             'site-relation': reverse(api + 'relation-list', request=request),
#             'conts-total': reverse(api + 'conts-total', request=request),
#             'site-contract': reverse(api + 'sitecontract-list', request=request),
#             # cash
#             'bank-code': reverse(api + 'bankcode-list', request=request),
#             'com-bank': reverse(api + 'com_bank-list', request=request),
#             'balance-by-acc': reverse(api + 'balance-by-acc', request=request),
#             'cashbook': reverse(api + 'cashbook-list', request=request),
#             'date-cashbook': reverse(api + 'date-cashbook', request=request),
#             'project-bank': reverse(api + 'project_bank-list', request=request),
#             'pr-balance-by-acc': reverse(api + 'pr-balance-by-acc', request=request),
#             'project-cashbook': reverse(api + 'project_cashbook-list', request=request),
#             'pr-date-cashbook': reverse(api + 'pr-date-cashbook', request=request),
#             'project-imprest': reverse(api + 'project-imprest-list', request=request),
#             'payment-list': reverse(api + 'payment-list', request=request),
#             'all-payment-list': reverse(api + 'all-payment-list', request=request),
#             'payment-sum': reverse(api + 'payment-sum', request=request),
#             'cont-count': reverse(api + 'cont-count', request=request),
#             'price': reverse(api + 'price-list', request=request),
#             'pay-order': reverse(api + 'install_order-list', request=request),
#             'down-payment': reverse(api + 'downpay-list', request=request),
#             # 'over-due-rule': reverse(apiV1 + OverDueRuleList.name, request=request),
#             # contract
#             'order-group': reverse(api + 'order_group-list', request=request),
#             'contract': reverse(api + 'contract-list', request=request),
#             'contract-set': reverse(api + 'contract-set-list', request=request),
#             'subs-sum': reverse(api + 'subs-summary', request=request),
#             'cont-sum': reverse(api + 'cont-summary', request=request),
#             'contractor': reverse(api + 'contractor-list', request=request),
#             'contractor-address': reverse(api + 'cont_address-list', request=request),
#             'contractor-contact': reverse(api + 'contact-list', request=request),
#             'contractor-release': reverse(api + 'release-list', request=request),
#             # notice
#             'sales-bill-issue': reverse(api + 'bill-list', request=request),
#             # document
#             'group': reverse(api + 'group-list', request=request),
#             'board': reverse(api + 'board-list', request=request),
#             'category': reverse(api + 'category-list', request=request),
#             'suitcase': reverse(api + 'suitcase-list', request=request),
#             'post': reverse(api + 'post-list', request=request),
#             # 'like': reverse(api + 'like-list', request=request),
#             # 'dislike': reverse(api + 'dislike-list', request=request),
#             'link': reverse(api + 'link-list', request=request),
#             'image': reverse(api + 'image-list', request=request),
#             'file': reverse(api + 'file-list', request=request),
#             'comment': reverse(api + 'comment-list', request=request),
#             'tag': reverse(api + 'tag-list', request=request),
#         })
