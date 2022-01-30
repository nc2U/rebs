from django.urls import path, include
from .views import *

app_name = 'rebs'

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('schedule/', memu2_1, name='menu2_1'),

    path('company/', include('company.urls')),
    # path('project/', include('project.urls')),
    # path('cash/', include('cash.urls')),
    # path('contract/', include('contract.urls')),
    # path('notice/', include('notice.urls')),
    # path('docs/', include('document.urls')),

    # pdf url
    # path('pdf-bill/', PdfExportBill.as_view(), name='pdf-bill'),
    # path('pdf-payments/', PdfExportPayments.as_view(), name='pdf-payments'),
]
