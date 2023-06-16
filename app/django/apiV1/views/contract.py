from django.db.models import Count, Sum
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet
from django_filters import ChoiceFilter, ModelChoiceFilter, DateFilter, BooleanFilter

from ..permission import *
from ..serializers.contract import *

from contract.models import (OrderGroup, Contract, ContractPrice, Contractor,
                             ContractorAddress, ContractorContact,
                             Succession, SuccessionBuyer, ContractorRelease)
from items.models import BuildingUnit


# Contract --------------------------------------------------------------------------
class OrderGroupViewSet(viewsets.ModelViewSet):
    queryset = OrderGroup.objects.all()
    serializer_class = OrderGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project', 'sort')
    search_fields = ('order_group_name',)


class ContractFilter(FilterSet):
    houseunit__isnull = BooleanFilter(field_name='keyunit__houseunit', lookup_expr='isnull', label='동호미지정 여부')
    keyunit__houseunit__building_unit = ModelChoiceFilter(queryset=BuildingUnit.objects.all(), label='동(건물)')
    contractor__status = ChoiceFilter(field_name='contractor__status', choices=Contractor.STATUS_CHOICES, label='현재상태')
    contractor__is_registed = BooleanFilter(field_name='contractor__is_registed', label='인가등록여부')
    from_contract_date = DateFilter(field_name='contractor__contract_date', lookup_expr='gte', label='계약일자부터')
    to_contract_date = DateFilter(field_name='contractor__contract_date', lookup_expr='lte', label='계약일자까지')

    class Meta:
        model = Contract
        fields = ('project', 'order_group', 'activation', 'unit_type', 'houseunit__isnull',
                  'keyunit__houseunit__building_unit', 'contractor__status',
                  'contractor__is_registed', 'from_contract_date', 'to_contract_date')


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_class = ContractFilter
    search_fields = ('serial_number', 'contractor__name', 'contractor__note',
                     'contractor__contractorcontact__cell_phone')
    ordering_fields = ('created_at', 'contractor__contract_date',
                       'serial_number', 'contractor__name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContractSetViewSet(ContractViewSet):
    serializer_class = ContractSetSerializer


class ContractPriceViewSet(viewsets.ModelViewSet):
    queryset = ContractPrice.objects.all()
    serializer_class = ContractPriceSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('contract__project', 'contract__order_group',
                        'contract__unit_type', 'contract__activation',
                        'contract__contractor__status')


class SubsSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = SubsSummarySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)

    def get_queryset(self):
        return Contract.objects.filter(activation=True, contractor__status=1) \
            .values('unit_type') \
            .annotate(num_cont=Count('unit_type'))


class ContSumFilter(FilterSet):
    to_contract_date = DateFilter(field_name='contractor__contract_date', lookup_expr='lte', label='계약일자까지')

    class Meta:
        model = Contract
        fields = ('project', 'to_contract_date')


class ContSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = ContSummarySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_class = ContSumFilter

    def get_queryset(self):
        return Contract.objects.filter(activation=True, contractor__status=2) \
            .values('order_group', 'unit_type') \
            .annotate(conts_num=Count('order_group')) \
            .annotate(price_sum=Sum('contractprice__price'))


class ContractorViewSet(viewsets.ModelViewSet):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('contract__project', 'gender', 'is_registed', 'status', 'is_active')
    search_fields = ('name', 'note', 'contract__serial_number')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContAddressViewSet(viewsets.ModelViewSet):
    queryset = ContractorAddress.objects.all()
    serializer_class = ContractorAddressSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContContactViewSet(viewsets.ModelViewSet):
    queryset = ContractorContact.objects.all()
    serializer_class = ContractorContactSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SuccessionViewSet(viewsets.ModelViewSet):
    queryset = Succession.objects.all()
    serializer_class = SuccessionSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SuccessionBuyerViewSet(viewsets.ModelViewSet):
    queryset = SuccessionBuyer.objects.all()
    serializer_class = SuccessionBuyerSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContReleaseViewSet(viewsets.ModelViewSet):
    queryset = ContractorRelease.objects.all().order_by('-request_date', '-created_at')
    serializer_class = ContractorReleaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project', 'status')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
