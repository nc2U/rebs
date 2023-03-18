from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportMixin

from .models import UnitType, UnitFloorType, KeyUnit, BuildingUnit, HouseUnit


class UnitTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    # form = UnitTypeForm
    list_display = (
        'id', 'project', 'name', 'sort', 'styled_color', 'actual_area', 'supply_area', 'contract_area', 'average_price',
        'num_unit')
    list_display_links = ('project', 'name',)
    list_editable = ('sort', 'actual_area', 'supply_area', 'contract_area', 'average_price', 'num_unit')
    list_filter = ('project',)

    def styled_color(self, obj):
        return format_html(f'<div style="width:15px; background:{obj.color};">&nbsp;</div>')

    styled_color.short_description = '타입색상'


class UnitFloorTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'start_floor', 'end_floor', 'extra_cond', 'alias_name')
    list_display_links = ('project',)
    list_editable = ('start_floor', 'end_floor', 'extra_cond', 'alias_name')
    list_filter = ('project',)


class KeyUnitAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'unit_code', 'unit_type', 'contract')
    search_fields = ('unit_code',)
    list_display_links = ('project', 'unit_code',)
    list_filter = ('project', 'unit_type', 'contract')


class BuindingUnitAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'name')
    list_display_links = ('project',)
    list_editable = ('name',)
    list_filter = ('project',)


class HouseUnitAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'key_unit', 'unit_type', 'building_unit',
        'name', 'floor_type', 'bldg_line', 'floor_no', 'is_hold', 'hold_reason')
    search_fields = ('name',)
    list_display_links = ('project', 'building_unit', 'name')
    list_filter = ('project', 'unit_type', 'building_unit', 'bldg_line', 'floor_type', 'is_hold', 'key_unit')


admin.site.register(UnitType, UnitTypeAdmin)
admin.site.register(UnitFloorType, UnitFloorTypeAdmin)
admin.site.register(KeyUnit, KeyUnitAdmin)
admin.site.register(BuildingUnit, BuindingUnitAdmin)
admin.site.register(HouseUnit, HouseUnitAdmin)
