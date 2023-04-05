from django.urls import path
from django.views.generic import RedirectView
from .views import superuser_check, create_superuser, create_company

app_name = 'install'

urlpatterns = [
    path('', superuser_check),
    path('create/superuser/', create_superuser, name='create_superuser'),
    path('create/company/', create_company, name='create_company'),
    # path('', include('django.contrib.auth.urls')),
    # path('register/', UserCreateView.as_view(), name='register'),
    # path('register/done/', UserCreateDoneTV.as_view(), name='register_done'),
]
