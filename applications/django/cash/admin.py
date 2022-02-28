from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from import_export.admin import ImportExportMixin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

from .models import (CompanyBankAccount, ProjectBankAccount, CashBook, ProjectCashBook,
                     SalesPriceByGT, InstallmentPaymentOrder, DownPayment, OverDueRule)


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
    list_display = ('id', 'deal_date', 'sort', 'account_d1', 'account_d2', 'account_d3',
                    'content', 'trader', 'bank_account', 'formatted_income', 'formatted_outlay', 'user')
    search_fields = ('account_d3', 'content', 'trader', 'note')
    list_display_links = ('deal_date', 'content')
    list_filter = (('deal_date', DateRangeFilter),)

    def formatted_income(self, obj):
        return f'{intcomma(obj.income)} 원' if obj.income else '-'

    def formatted_outlay(self, obj):
        return f'{intcomma(obj.outlay)} 원' if obj.outlay else '-'

    formatted_income.short_description = '입금액'
    formatted_outlay.short_description = '출금액'


class ProjectCashBookAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'deal_date', 'sort', 'project_account_d1', 'project_account_d2', 'contract',
        'installment_order', 'content', 'trader', 'bank_account', 'formatted_income', 'formatted_outlay', 'created_at',
        'updated_at', 'user')
    search_fields = ('content', 'trader', 'note')
    list_display_links = ('project', 'deal_date')
    list_filter = ('sort', 'project_account_d1', 'project_account_d2', 'is_contract_payment', 'bank_account')

    def formatted_income(self, obj):
        return f'{intcomma(obj.income)} 원' if obj.income else '-'

    def formatted_outlay(self, obj):
        return f'{intcomma(obj.outlay)} 원' if obj.outlay else '-'

    formatted_income.short_description = '입금액'
    formatted_outlay.short_description = '출금액'


class SalesPriceByGTAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'order_group', 'unit_type', 'unit_floor_type', 'price_build', 'price_land', 'price_tax',
        'price')
    list_display_links = ('project', 'unit_type', 'unit_floor_type')
    list_editable = ('price_build', 'price_land', 'price_tax', 'price')
    list_filter = ('project', 'order_group', 'unit_type')


class InstallmentPaymentOrderAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'pay_name', 'pay_sort', 'pay_code', 'pay_time', 'alias_name', 'is_pm_cost', 'pay_due_date',
        'extra_due_date')
    search_fields = ('pay_name', 'alias_name',)
    list_editable = ('alias_name', 'is_pm_cost', 'pay_due_date', 'extra_due_date')
    list_display_links = ('project', 'pay_name',)


class DownPaymentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'order_group', 'unit_type', 'number_payments', 'payment_amount')
    list_display_links = ('project', 'order_group', 'unit_type')
    list_editable = ('number_payments', 'payment_amount')
    list_filter = ('order_group', 'unit_type')


class OverDueRuleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', '__str__', 'term_start', 'term_end', 'rate_year')
    list_display_links = ('__str__',)
    list_editable = ('term_start', 'term_end', 'rate_year')
    list_filter = ('project',)


admin.site.register(CompanyBankAccount, CompanyBankAccountAdmin)
admin.site.register(ProjectBankAccount, ProjectBankAccountAdmin)
admin.site.register(CashBook, CashBookAdmin)
admin.site.register(ProjectCashBook, ProjectCashBookAdmin)
admin.site.register(SalesPriceByGT, SalesPriceByGTAdmin)
admin.site.register(InstallmentPaymentOrder, InstallmentPaymentOrderAdmin)
admin.site.register(DownPayment, DownPaymentAdmin)
admin.site.register(OverDueRule, OverDueRuleAdmin)
