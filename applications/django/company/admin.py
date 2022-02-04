from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Company, Department, Position, Staff


class DepartmentInline(admin.StackedInline):
    model = Department


class PositionInline(admin.StackedInline):
    model = Position


class CompanyAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'name', 'ceo', 'tax_number', 'org_number', 'business_cond', 'business_even', 'es_date', 'op_date')
    list_display_links = ('name',)
    inlines = (DepartmentInline, PositionInline)


class DepartmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'task')
    list_display_links = ('name',)


class PositionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'rank', 'title')
    list_display_links = ('title',)


class StaffAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'birth_date', 'entered_date', 'email', 'status')
    list_display_links = ('name',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Staff, StaffAdmin)
