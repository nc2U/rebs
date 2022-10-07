from django.urls import path
from .views import *

app_name = 'excel'

urlpatterns = [
    path('contracts/', ExportContracts.as_view(), name='contracts'),
    path('reservations/', ExportApplicants.as_view(), name='reservations'),
    path('releases/', ExportReleases.as_view(), name='releases'),
    path('status/', ExportUnitStatus.as_view(), name='unit-status'),
    path('payments/', export_payments_xls, name='payments'),
    path('p-balance/', ExportProjectBalance.as_view(), name='project-balance'),
    path('p-daily-cash/', export_project_daily_cash_xls, name='project-daily-cash'),
    path('p-budget/', ExportBudgetExecutionStatus.as_view(), name='budget'),
    path('p-cashbook/', export_project_cash_xls, name='project-cash'),
    path('sites/', export_sites_xls, name='sites'),
    path('sites-by-owner/', export_sitesByOwner_xls, name='sites-by-owner'),
    path('sites-contracts/', export_sitesContracts_xls, name='sites-contracts'),
    path('balance/', export_cash_balance_xls, name='balance'),
    path('daily-cash/', export_daily_cash_xls, name='daily-cash'),
    path('cashbook/', export_cashbook_xls, name='cashbook'),
]
