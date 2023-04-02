from rest_framework.routers import DefaultRouter

from .views import accounts
from .views import company
from .views import rebs
from .views import project
from .views import items
from .views import payment
from .views import cash
from .views import contract
from .views import notice
from .views import document

app_name = 'api'

router = DefaultRouter()
# accounts
router.register(r'user', accounts.UserViewSet)
router.register(r'staff-auth', accounts.StaffAuthViewSet)
router.register(r'profile', accounts.ProfileViewSet)
router.register(r'todo', accounts.TodoViewSet)
# company
router.register(r'company', company.CompanyViewSet)
router.register(r'logo', company.LogoViewSet)
router.register(r'department', company.DepartmentViewSet)
router.register(r'all-departs', company.AllDepartsViewSet, basename='all-departs')
router.register(r'grade', company.JobGradeViewSet)
router.register(r'all-grades', company.AllGradesViewSet, basename='all-grades')
router.register(r'position', company.PositionViewSet)
router.register(r'all-positions', company.AllPositionsViewSet, basename='all-positions')
router.register(r'duty-title', company.DutyTitleViewSet)
router.register(r'all-dutys', company.AllDutyViewSet, basename='all-dutys')
router.register(r'staff', company.StaffViewSet)
# rebs
router.register(r'schedule', rebs.CalendarScheduleViewSet)
router.register(r'account-sort', rebs.AccountSortViewSet)  # only list
router.register(r'account-depth1', rebs.AccountSubD1ViewSet)  # only list
router.register(r'account-depth2', rebs.AccountSubD2ViewSet)  # only list
router.register(r'account-depth3', rebs.AccountSubD3ViewSet)  # only list
router.register(r'project-acc-sort', rebs.ProjectAccountSortViewSet)  # only list
router.register(r'project-account-depth1', rebs.ProjectAccountD1ViewSet)  # only list
router.register(r'project-account-depth3', rebs.ProjectAccountD3ViewSet)  # only list
router.register(r'wise-say', rebs.WiseSayViewSet)
# project
router.register(r'project', project.ProjectViewSet)
router.register(r'inc-budget', project.ProjectIncBudgetViewSet)  # only list
router.register(r'out-budget', project.ProjectOutBudgetViewSet)  # only list
router.register(r'status-budget', project.StatusOutBudgetViewSet, basename='status-budget')  # only list
router.register(r'exec-amount', project.ExecAmountToBudgetViewSet, basename='exec-amount')  # only list
router.register(r'site', project.SiteViewSet)
router.register(r'all-site', project.AllSiteViewSet, basename='all-site')  # only list
router.register(r'sites-total', project.TotalSiteAreaViewSet, basename='sites-total')  # only list
router.register(r'site-owner', project.SiteOwnerViewSet)
router.register(r'all-owner', project.AllOwnerViewSet, basename='all-owner')  # only list
router.register(r'owners-total', project.TotalOwnerAreaViewSet, basename='owners-total')  # only list
router.register(r'site-relation', project.SiteRelationViewSet)
router.register(r'site-contract', project.SiteContractViewSet)
router.register(r'conts-total', project.TotalContractedAreaViewSet, basename='conts-total')  # only list
# items
router.register(r'type', items.UnitTypeViewSet)
router.register(r'floor', items.UnitFloorTypeViewSet)
router.register(r'key-unit', items.KeyUnitViewSet)
router.register(r'bldg', items.BuildingUnitViewSet)
router.register(r'house-unit', items.HouseUnitViewSet)
router.register(r'available-house-unit', items.AvailableHouseUnitViewSet,
                basename='available-house-unit')  # only list
router.register(r'all-house-unit', items.AllHouseUnitViewSet, basename='all-house-unit')  # only list
router.register(r'unit-summary', items.HouseUnitSummaryViewSet, basename='unit-summary')
# payment
router.register(r'payment', payment.PaymentViewSet, basename='payment')  # only list
router.register(r'all-payment', payment.AllPaymentViewSet, basename='all-payment')  # only list
router.register(r'payment-sum', payment.PaymentSummaryViewSet, basename='payment-sum')  # only list
router.register(r'cont-num-type', payment.ContNumByTypeViewSet, basename='cont-num-type')  # only list
router.register(r'price', payment.SalesPriceViewSet)
router.register(r'pay-order', payment.InstallmentOrderViewSet)
router.register(r'down-payment', payment.DownPaymentViewSet)
# cash
router.register(r'bank-code', cash.BankCodeViewSet)
router.register(r'company-bank-account', cash.ComBankAccountViewSet)
router.register(r'balance-by-acc', cash.BalanceByAccountViewSet, basename='balance-by-acc')  # only list
router.register(r'cashbook', cash.CashBookViewSet)
router.register(r'date-cashbook', cash.DateCashBookViewSet, basename='date-cashbook')  # only list
router.register(r'project-bank-account', cash.ProjectBankAccountViewSet)
router.register(r'pr-balance-by-acc', cash.PrBalanceByAccountViewSet, basename='pr-balance-by-acc')  # only list
router.register(r'project-cashbook', cash.ProjectCashBookViewSet)
router.register(r'pr-date-cashbook', cash.ProjectDateCashBookViewSet, basename='pr-date-cashbook')  # only list
router.register(r'project-imprest', cash.ProjectImprestViewSet, basename='pr-imprest')  # only list
# contract
router.register(r'order-group', contract.OrderGroupViewSet)
router.register(r'contract', contract.ContractViewSet)
router.register(r'contract-set', contract.ContractSetViewSet, basename='cont-set')
router.register(r'cont-price', contract.ContractPriceViewSet)
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
router.register(r'all-suitcase', document.AllLawSuitCaseViewSet, basename='all-suitcase')
router.register(r'post', document.PostViewSet)
router.register(r'link', document.LinkViewSet)
router.register(r'image', document.ImageViewSet)
router.register(r'file', document.FileViewSet)
router.register(r'comment', document.CommentViewSet)
router.register(r'tag', document.TagViewSet)

urlpatterns = router.urls
