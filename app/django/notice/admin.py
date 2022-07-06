from django.contrib import admin
from .models import SalesBillIssue


class SalesBillIssueAdmin(admin.ModelAdmin):
    pass


admin.site.register(SalesBillIssue, SalesBillIssueAdmin)
