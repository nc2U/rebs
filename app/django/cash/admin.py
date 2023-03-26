from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from import_export.admin import ImportExportMixin
from rangefilter.filters import DateRangeFilter

from .models import CompanyBankAccount, ProjectBankAccount, CashBook, ProjectCashBook


class CompanyBankAccountAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'alias_name', 'division', 'bankcode', 'number', 'holder', 'open_date', 'note', 'inactive')
    list_display_links = ('alias_name',)
    list_filter = ('division', 'bankcode', 'holder')


class ProjectBankAccountAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'alias_name', 'bankcode', 'number', 'holder', 'open_date', 'note', 'inactive', 'directpay')
    list_display_links = ('project', 'alias_name',)
    list_filter = ('bankcode', 'holder')


class CashBookAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'deal_date', 'sort', 'account_d1', 'account_d2', 'account_d3', 'content',
                    'trader', 'bank_account', 'formatted_income', 'formatted_outlay', 'evidence', 'user')
    list_editable = ('evidence',)
    search_fields = ('account_d3', 'content', 'trader', 'note')
    list_display_links = ('deal_date', 'content')
    list_filter = (('deal_date', DateRangeFilter), 'sort', 'account_d1', 'account_d2', 'evidence')

    def formatted_income(self, obj):
        return f'{intcomma(obj.income)} 원' if obj.income else '-'

    def formatted_outlay(self, obj):
        return f'{intcomma(obj.outlay)} 원' if obj.outlay else '-'

    formatted_income.short_description = '입금액'
    formatted_outlay.short_description = '출금액'


class ProjectCashBookAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'deal_date', 'sort', 'project_account_d1', 'project_account_d2', 'is_imprest', 'contract',
        'installment_order', 'content', 'trader', 'bank_account', 'formatted_income', 'formatted_outlay', 'evidence',
        'user')
    list_editable = ('evidence',)
    search_fields = ('pk', 'content', 'trader', 'note')
    list_display_links = ('project', 'deal_date')
    list_filter = (
        'project', 'sort', ('deal_date', DateRangeFilter), 'project_account_d1',
        'project_account_d2', 'is_imprest', 'bank_account')

    def formatted_income(self, obj):
        return f'{intcomma(obj.income)} 원' if obj.income else '-'

    def formatted_outlay(self, obj):
        return f'{intcomma(obj.outlay)} 원' if obj.outlay else '-'

    formatted_income.short_description = '입금액'
    formatted_outlay.short_description = '출금액'


admin.site.register(CompanyBankAccount, CompanyBankAccountAdmin)
admin.site.register(ProjectBankAccount, ProjectBankAccountAdmin)
admin.site.register(CashBook, CashBookAdmin)
admin.site.register(ProjectCashBook, ProjectCashBookAdmin)
