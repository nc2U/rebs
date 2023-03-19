from django.urls import path
from .views import *

app_name = 'pdf'

urlpatterns = [
    # pdf url
    path('bill/', PdfExportBill.as_view(), name='bill'),
    path('payments/', PdfExportPayments.as_view(), name='payments'),
]
