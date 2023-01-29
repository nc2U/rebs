from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Company, Logo, Department, JobRank, Staff


class DepartmentInline(admin.StackedInline):
    model = Department


class JobRankInline(admin.StackedInline):
    model = JobRank


class LogoInline(admin.StackedInline):
    model = Logo


class CompanyAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'name', 'ceo', 'tax_number', 'org_number', 'business_cond', 'business_even', 'es_date', 'op_date')
    list_display_links = ('name',)
    inlines = (LogoInline, DepartmentInline, JobRankInline)


class DepartmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'task')
    list_display_links = ('name',)


class JobRankAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'sort', 'rank', 'title')
    list_display_links = ('rank',)


class StaffAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'birth_date', 'entered_date', 'email', 'status')
    list_display_links = ('name',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(JobRank, JobRankAdmin)
admin.site.register(Staff, StaffAdmin)
