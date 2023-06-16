from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import (OrderGroup, Contract, ContractPrice,
                     Contractor, ContractorAddress, ContractorContact,
                     Succession, SuccessionBuyer, ContractorRelease)


class OrderGroupAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'order_group_name', 'order_number', 'sort')
    list_display_links = ('project', 'order_group_name',)


class ContractorInline(admin.StackedInline):
    model = Contractor
    extra = 0


class ContractPriceInline(admin.StackedInline):
    model = ContractPrice
    extra = 0


class ContractAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'serial_number',
                    'order_group', 'unit_type', 'user', 'activation')
    list_display_links = ('project', 'serial_number',)
    list_filter = ('activation',)
    search_fields = ('serial_number',)
    inlines = [ContractorInline, ContractPriceInline]


class CAdressInline(ImportExportMixin, admin.StackedInline):
    model = ContractorAddress
    extra = 0


class CContactInline(ImportExportMixin, admin.TabularInline):
    model = ContractorContact
    extra = 0


class ContactorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'birth_date', 'gender', 'is_registed',
                    'status', 'is_active', 'reservation_date', 'contract_date')
    search_fields = ('name',)
    list_display_links = ('name',)
    list_filter = ('contract_date', 'gender', 'is_registed', 'status')
    list_editable = ('gender', 'is_registed', 'is_active')
    inlines = (CContactInline, CAdressInline)


class CAdressAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'id_zipcode', 'id_address1', 'id_address2', 'id_address3',
                    'dm_zipcode', 'dm_address1', 'dm_address2', 'dm_address3')


class CContactAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'cell_phone', 'home_phone', 'other_phone', 'email')


class SuccessionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('pk', 'contract', 'seller', 'buyer', 'apply_date', 'trading_date',
                    'is_approval', 'approval_date', 'user')
    search_fields = ('seller', 'buyer')
    list_display_links = ('contract', 'seller', 'buyer')
    list_editable = ('is_approval', 'approval_date')


class SuccessionBuyerAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('pk', 'name', 'birth_date', 'gender', 'cell_phone', 'email', 'user')
    search_fields = ('name', 'cell_phone', 'email')
    list_display_links = ('name', 'birth_date')


class ContractorReleaseAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'contractor', 'status', 'refund_amount',
                    'refund_account_bank', 'refund_account_number',
                    'refund_account_depositor', 'request_date', 'completion_date')
    list_editable = ('request_date', 'completion_date')


admin.site.register(OrderGroup, OrderGroupAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Contractor, ContactorAdmin)
admin.site.register(ContractorAddress, CAdressAdmin)
admin.site.register(ContractorContact, CContactAdmin)
admin.site.register(Succession, SuccessionAdmin)
admin.site.register(SuccessionBuyer, SuccessionBuyerAdmin)
admin.site.register(ContractorRelease, ContractorReleaseAdmin)
