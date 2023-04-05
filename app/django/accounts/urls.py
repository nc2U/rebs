from django.urls import path
from django.views.generic import RedirectView
from .views import create_superuser

app_name = 'install'

urlpatterns = [
    path('', RedirectView.as_view(url='/install/create/superuser/'), name='install'),
    path('create/superuser/', create_superuser, name='create_superuser')
    # path('', include('django.contrib.auth.urls')),
    # path('register/', UserCreateView.as_view(), name='register'),
    # path('register/done/', UserCreateDoneTV.as_view(), name='register_done'),
]
