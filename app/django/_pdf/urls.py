from django.urls import path
from .views import *

app_name = 'pdf'

urlpatterns = [
    # pdf url
    path('pdf-bill/', PdfExportBill.as_view(), name='pdf-bill'),
    path('pdf-payments/', PdfExportPayments.as_view(), name='pdf-payments'),
]
