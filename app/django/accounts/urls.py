from django.urls import path, include

from .views import UserCreateView, UserCreateDoneTV, create_superuser

app_name = 'setup'

urlpatterns = [
    path('create/superuser/', create_superuser, name='create_superuser')
    # path('', include('django.contrib.auth.urls')),
    # path('register/', UserCreateView.as_view(), name='register'),
    # path('register/done/', UserCreateDoneTV.as_view(), name='register_done'),
]
