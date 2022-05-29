"""_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
)
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from django.conf.urls.static import static

url = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('accounts/', include('allauth.urls')),
    # path('accounts/', include('accounts.urls')),
    path('', include('django.contrib.auth.urls')),

    path('', TemplateView.as_view(template_name='index.html')),

    path('rebs/', RedirectView.as_view(url='/rebs/dashboard/'), name='home'),
    path('rebs/', include('rebs.urls')),
    path('book/', include('book.urls')),

    path('excel/', include('excel.urls')),
    path('mdeditor/', include('mdeditor.urls')),
    path('tinymce/', include('tinymce.urls')),
]

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
urlpatterns = url if AWS_STORAGE_BUCKET_NAME else url + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
