from django.contrib.auth.decorators import login_required
from django.urls import path

from contract.exports.pdf import PdfExportCertOccupancy
from notice.exports.pdf import PdfExportBill
from payment.exports.pdf import (
    PdfExportLedgerPayment, PdfExportLedgerDailyLateFee, PdfExportLedgerCalculation
)
from work.exports.pdf import PdfExportMeeting

app_name = 'pdf'

urlpatterns = [
    # Notice 관련
    path('bill/', login_required(PdfExportBill.as_view()), name='bill'),

    # Payment 관련
    path('ledger/payment/', login_required(PdfExportLedgerPayment.as_view()), name='ledger-payment'),
    path('ledger/daily-late-fee/', login_required(PdfExportLedgerDailyLateFee.as_view()), name='ledger-daily-late-fee'),
    path('ledger/calculation/', login_required(PdfExportLedgerCalculation.as_view()), name='ledger-calculation'),

    # Contract 관련
    path('cert-occupancy/', login_required(PdfExportCertOccupancy.as_view()), name='cert-occupancy'),

    # Work 관련
    path('work/meeting/<int:pk>/', PdfExportMeeting.as_view(), name='work-meeting'),
]
