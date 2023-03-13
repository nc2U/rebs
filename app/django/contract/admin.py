from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import OrderGroup, Contract, Contractor, ContractorAddress, ContractorContact, ContractorRelease


class OrderGroupAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'order_group_name', 'order_number', 'sort')
    list_display_links = ('project', 'order_group_name',)


class ContractorInline(admin.StackedInline):
    model = Contractor
    extra = 0


class ContractAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'serial_number', 'order_group',
                    'unit_type', 'user', 'activation')
    list_display_links = ('project', 'serial_number',)
    list_filter = ('activation',)
    search_fields = ('serial_number',)
    inlines = [ContractorInline]


class CAdressInline(ImportExportMixin, admin.StackedInline):
    model = ContractorAddress
    extra = 0


class CContactInline(ImportExportMixin, admin.TabularInline):
    model = ContractorContact
    extra = 0


class ContactorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'birth_date', 'gender', 'is_registed',
                    'status', 'reservation_date', 'contract_date')
    search_fields = ('name',)
    list_display_links = ('name',)
    list_filter = ('contract_date', 'gender', 'is_registed', 'status')
    list_editable = ('gender', 'is_registed')
    inlines = (CContactInline, CAdressInline)


class CAdressAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'id_zipcode', 'id_address1', 'id_address2', 'id_address3',
                    'dm_zipcode', 'dm_address1', 'dm_address2', 'dm_address3')


class CContactAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'cell_phone', 'home_phone', 'other_phone', 'email')


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
admin.site.register(ContractorRelease, ContractorReleaseAdmin)
