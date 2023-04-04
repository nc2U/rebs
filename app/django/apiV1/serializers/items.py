from rest_framework import serializers

from contract.models import Contract, Contractor
from items.models import UnitType, UnitFloorType, KeyUnit, BuildingUnit, HouseUnit


# Items --------------------------------------------------------------------------
class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = (
            'pk', 'project', 'name', 'sort', 'color', 'actual_area',
            'supply_area', 'contract_area', 'average_price', 'num_unit')


class SimpleUnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = ('pk', 'name', 'color', 'average_price')


class UnitFloorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitFloorType
        fields = ('pk', 'project', 'start_floor', 'end_floor', 'extra_cond', 'alias_name')


class BuildingUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingUnit
        fields = ('pk', 'project', 'name')


class KeyUnitSerializer(serializers.ModelSerializer):
    houseunit = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = KeyUnit
        fields = ('pk', 'project', 'unit_type', 'unit_code', 'houseunit', 'contract')


class HouseUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseUnit
        fields = ('pk', 'unit_type', 'floor_type', '__str__', 'building_unit',
                  'name', 'key_unit', 'bldg_line', 'floor_no', 'is_hold', 'hold_reason')


class ContractorInContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('status', 'name')


class ContractInKeyUnitSerializer(serializers.ModelSerializer):
    contractor = ContractorInContractSerializer()

    class Meta:
        model = Contract
        fields = ('pk', 'contractor')


class KeyUnitInHouseUnitSerializer(serializers.ModelSerializer):
    contract = ContractInKeyUnitSerializer()

    class Meta:
        model = KeyUnit
        fields = ('pk', 'contract')


class AllHouseUnitSerializer(serializers.ModelSerializer):
    key_unit = KeyUnitInHouseUnitSerializer()

    class Meta:
        model = HouseUnit
        fields = ('pk', 'unit_type', 'floor_type', 'building_unit', 'name',
                  'key_unit', 'bldg_line', 'floor_no', 'is_hold')


class HouseUnitSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseUnit
        fields = ('pk', 'unit_type', 'building_unit', 'name')
