from django.urls import path
from .views import *

app_name = 'cash-inout'

urlpatterns = [
    path('dayly-report/', DaylyCashReport.as_view(), name='report'),
    path('', CashInoutLV.as_view(), name='index'),
    path('create/', CashInoutCV.as_view(), name='create'),
    path('update/<int:pk>/', CashInoutUV.as_view(), name='update'),
    path('delete/<int:pk>/', CashInoutDV, name='delete'),

    path('project/report/', ProjectCashReport.as_view(), name='project-report'),
    path('project/', ProjectCashInoutLV.as_view(), name='project-index'),
    path('project/create/', ProjectCashInoutCV.as_view(), name='project-create'),
    path('project/update/<int:pk>/', ProjectCashInoutUV.as_view(), name='project-update'),
    path('project/delete/<int:pk>/', ProjectCashInoutDV, name='project-delete'),

    path('project/payment/', SalesPaymentLV.as_view(), name='payment-index'),
    path('project/payment/register/', SalesPaymentRegister.as_view(), name='payment-register'),
    path('project/payment/delete/<int:pk>/', paymentDeleteView, name='payment-delete'),
]
