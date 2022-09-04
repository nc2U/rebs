from django.db.models import Count
from rest_framework import generics
from django_filters.rest_framework import FilterSet
from django_filters import ChoiceFilter, ModelChoiceFilter, DateFilter, BooleanFilter

from ..permission import *
from ..serializers.contract import *

from project.models import (Project, UnitType, UnitFloorType,
                            KeyUnit, BuildingUnit, HouseUnit, ProjectBudget,
                            Site, SiteOwner, SiteOwnshipRelationship, SiteContract)

from contract.models import (OrderGroup, Contract, Contractor,
                             ContractorAddress, ContractorContact, ContractorRelease)


# Contract --------------------------------------------------------------------------
class OrderGroupList(generics.ListCreateAPIView):
    name = 'order_group-list'
    queryset = OrderGroup.objects.all()
    serializer_class = OrderGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project', 'sort')
    search_fields = ('order_group_name',)


class OrderGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'order_group-detail'
    queryset = OrderGroup.objects.all()
    serializer_class = OrderGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContractFilter(FilterSet):
    keyunit__houseunit__building_unit = ModelChoiceFilter(queryset=BuildingUnit.objects.all(), label='동(건물)')
    contractor__status = ChoiceFilter(field_name='contractor__status', choices=Contractor.STATUS_CHOICES, label='현재상태')
    contractor__is_registed = BooleanFilter(field_name='contractor__is_registed', label='인가등록여부')
    from_contract_date = DateFilter(field_name='contractor__contract_date', lookup_expr='gte', label='계약일자부터')
    to_contract_date = DateFilter(field_name='contractor__contract_date', lookup_expr='lte', label='계약일자까지')

    class Meta:
        model = Contract
        fields = ('project', 'order_group', 'activation', 'unit_type',
                  'keyunit__houseunit__building_unit', 'contractor__status',
                  'contractor__is_registed', 'from_contract_date', 'to_contract_date')


class ContractList(generics.ListCreateAPIView):
    name = 'contract-list'
    queryset = Contract.objects.all()
    serializer_class = ContractListSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_class = ContractFilter
    search_fields = (
        'serial_number', 'contractor__name', 'contractor__note', 'contractor__contractorcontact__cell_phone')
    ordering_fields = (
        'created_at', 'contractor__contract_date', 'serial_number', 'contractor__name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'contract-detail'
    queryset = Contract.objects.all()
    serializer_class = ContractListSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContractCustomList(ContractList):
    name = 'contract-cumstom-list'
    serializer_class = ContractCustomListSerializer


class ContractCustomDetail(ContractDetail):
    name = 'contract-custom-detail'
    serializer_class = ContractCustomListSerializer


class SubsSummaryList(generics.ListAPIView):
    name = 'subs-summary'
    serializer_class = SubsSummarySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def get_queryset(self):
        return Contract.objects.filter(activation=True, contractor__status=1) \
            .values('unit_type') \
            .annotate(num_cont=Count('unit_type'))


class ContSummaryList(generics.ListAPIView):
    name = 'cont-summary'
    serializer_class = ContSummarySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def get_queryset(self):
        return Contract.objects.filter(activation=True, contractor__status=2) \
            .values('order_group', 'unit_type') \
            .annotate(num_cont=Count('order_group'))


class ContractorList(generics.ListCreateAPIView):
    name = 'contractor-list'
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('gender', 'is_registed', 'status')
    search_fields = ('name', 'note', 'contract__serial_number')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContractorDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'contractor-detail'
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContAddressList(generics.ListCreateAPIView):
    name = 'cont_address-list'
    queryset = ContractorAddress.objects.all()
    serializer_class = ContractorAddressSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContAddressDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'cont_address-detail'
    queryset = ContractorAddress.objects.all()
    serializer_class = ContractorAddressSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContContactList(generics.ListCreateAPIView):
    name = 'contact-list'
    queryset = ContractorContact.objects.all()
    serializer_class = ContractorContactSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContContactDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'contact-detail'
    queryset = ContractorContact.objects.all()
    serializer_class = ContractorContactSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContReleaseList(generics.ListCreateAPIView):
    name = 'release-list'
    queryset = ContractorRelease.objects.all().order_by('-request_date')
    serializer_class = ContractorReleaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filter_fields = ('project',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContReleaseDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'release-detail'
    queryset = ContractorRelease.objects.all()
    serializer_class = ContractorReleaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
