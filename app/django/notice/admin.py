from django.contrib import admin
from .models import SalesBillIssue


@admin.register(SalesBillIssue)
class SalesBillIssueAdmin(admin.ModelAdmin):
    pass
