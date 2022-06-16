from django.urls import path, include

from .views import UserCreateView, UserCreateDoneTV

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', UserCreateView.as_view(), name='register'),
    path('register/done/', UserCreateDoneTV.as_view(), name='register_done'),
]
