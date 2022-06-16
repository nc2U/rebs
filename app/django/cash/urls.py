from django.urls import path
from .views import *

app_name = 'cash-inout'

urlpatterns = [
    path('dayly-report/', DaylyCashReport.as_view(), name='report'),
    path('cash/', CashInoutLV.as_view(), name='index'),
    path('cash/create/', CashInoutCV.as_view(), name='create'),
    path('cash/update/<int:pk>/', CashInoutUV.as_view(), name='update'),
    path('cash/delete/<int:pk>/', CashInoutDV, name='delete'),
    path('project-cash/report/', ProjectCashReport.as_view(), name='project-report'),
    path('project-cash/', ProjectCashInoutLV.as_view(), name='project-index'),
    path('project-cash/create/', ProjectCashInoutCV.as_view(), name='project-create'),
    path('project-cash/update/<int:pk>/', ProjectCashInoutUV.as_view(), name='project-update'),
    path('project-cash/delete/<int:pk>/', ProjectCashInoutDV, name='project-delete'),
    path('project-cash/payment/', SalesPaymentLV.as_view(), name='payment-index'),
    path('project-cash/payment/register/', SalesPaymentRegister.as_view(), name='payment-register'),
    path('project-cash/payment/delete/<int:pk>/', paymentDeleteView, name='payment-delete'),
]
