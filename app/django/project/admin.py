from django.contrib import admin
from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import intcomma
from import_export.admin import ImportExportMixin

from .models import (Project, UnitType, UnitFloorType, KeyUnit,
                     BuildingUnit, HouseUnit, ProjectBudget,
                     Site, SiteOwner, SiteOwnshipRelationship, SiteContract)


class ProjectAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'kind', 'num_unit', 'build_size', 'area_usage')
    list_display_links = ('name',)
    list_editable = ('order', 'kind', 'num_unit', 'build_size', 'area_usage')


class UnitTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    # form = UnitTypeForm
    list_display = (
        'id', 'project', 'name', 'styled_color', 'actual_area', 'supply_area', 'contract_area', 'average_price',
        'num_unit')
    list_display_links = ('project', 'name',)
    list_editable = ('actual_area', 'supply_area', 'contract_area', 'average_price', 'num_unit')

    def styled_color(self, obj):
        return format_html(f'<div style="width:15px; background:{obj.color};">&nbsp;</div>')

    styled_color.short_description = '타입색상'


class UnitFloorTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'start_floor', 'end_floor', 'extra_cond', 'alias_name')
    list_display_links = ('project',)
    list_editable = ('start_floor', 'end_floor', 'extra_cond', 'alias_name')


class KeyUnitAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'unit_code', 'unit_type', 'contract')
    search_fields = ('unit_code',)
    list_display_links = ('project', 'unit_code',)
    list_filter = ('project', 'unit_type', 'contract',)


class BuindingUnitAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'name')
    list_display_links = ('project',)
    list_editable = ('name',)


class HouseUnitAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'key_unit', 'unit_type', 'building_unit',
        'name', 'floor_type', 'bldg_line', 'floor_no', 'is_hold', 'hold_reason')
    search_fields = ('name',)
    list_display_links = ('project', 'key_unit',)


class ProjectBudgetAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'account_d1', 'account_d2', 'budget')
    list_display_links = ('project', 'account_d1', 'account_d2')
    list_editable = ('budget',)


class SiteAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'order', 'project', '__str__', 'site_purpose', 'official_area',
        'returned_area', 'dup_issue_date', 'rights_restrictions')
    list_display_links = ('project', '__str__',)
    list_editable = ('official_area', 'returned_area')
    search_fields = ('__str__',)
    list_filter = ('project',)


class SiteOwnerAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'owner', 'date_of_birth', 'phone1', 'phone2', 'zipcode', 'address1', 'address2', 'address3', 'own_sort')
    list_display_links = ('owner',)
    search_fields = ('owner', 'own_sort')
    list_filter = ('project', 'own_sort',)


class SiteOwnshipRelationshipAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'site', 'site_owner', 'ownership_ratio', 'owned_area', 'acquisition_date')
    list_display_links = ('site', 'site_owner')
    list_editable = ('ownership_ratio', 'owned_area', 'acquisition_date')


class SiteContractAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'owner', 'formatted_price', 'contract_date', 'acc_bank', 'acc_number', 'acc_owner', 'remain_pay_is_paid',
        'ownership_completion')
    list_display_links = ('owner',)

    def formatted_price(self, obj):
        price = intcomma(obj.total_price)
        return f'{price} 원'

    formatted_price.short_description = '총매매대금'


admin.site.register(Project, ProjectAdmin)
admin.site.register(UnitType, UnitTypeAdmin)
admin.site.register(UnitFloorType, UnitFloorTypeAdmin)
admin.site.register(KeyUnit, KeyUnitAdmin)
admin.site.register(BuildingUnit, BuindingUnitAdmin)
admin.site.register(HouseUnit, HouseUnitAdmin)
admin.site.register(ProjectBudget, ProjectBudgetAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(SiteOwner, SiteOwnerAdmin)
admin.site.register(SiteOwnshipRelationship, SiteOwnshipRelationshipAdmin)
admin.site.register(SiteContract, SiteContractAdmin)
