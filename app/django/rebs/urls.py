from django.urls import path, include
from .views import *

app_name = 'rebs'

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('schedule/', menu2_1, name='menu2_1'),

    path('cash/', include('cash.urls')),
    path('company/', include('company.urls')),
    path('project/', include('project.urls')),
    path('contract/', include('contract.urls')),
    path('notice/', include('notice.urls')),
    path('docs/', include('document.urls')),
]
