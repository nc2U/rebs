from django.urls import path
from .views import *

app_name = 'contract'

urlpatterns = [
    path('', ContractLV.as_view(), name='index'),
    path('register/', ContractRegisterView.as_view(), name='register'),
    path('contractor/<int:pk>/', ContractorUpdate.as_view(), name='contractor'),
    path('trans/<int:pk>/', ContractorTrans.as_view(), name='trans'),
    path('release/register/', ContractorReleaseRegister.as_view(), name='release'),
    path('dashboard/', BuildDashboard.as_view(), name='dashboard'),
]
