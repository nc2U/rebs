from datetime import datetime
from django.db.models import Sum, F, Q, Case, When
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet
from django_filters import BooleanFilter

from ..permission import *
from ..pagination import *
from ..serializers.project import *

from project.models import (Project, UnitType, ProjectIncBudget, ProjectOutBudget,
                            UnitFloorType, KeyUnit, BuildingUnit, HouseUnit,
                            Site, SiteOwner, SiteOwnshipRelationship, SiteContract)

from cash.models import BankCode, CompanyBankAccount, ProjectBankAccount, CashBook, ProjectCashBook

TODAY = datetime.today().strftime('%Y-%m-%d')


# Project --------------------------------------------------------------------------
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class UnitTypeViewSet(viewsets.ModelViewSet):
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)
    search_fields = ('name',)


class ProjectIncBudgetViewSet(viewsets.ModelViewSet):
    queryset = ProjectIncBudget.objects.all()
    serializer_class = ProjectIncBudgetSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project', 'unit_type__sort')


class ProjectOutBudgetViewSet(viewsets.ModelViewSet):
    queryset = ProjectOutBudget.objects.all()
    serializer_class = ProjectOutBudgetSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)


class StatusOutBudgetViewSet(ProjectOutBudgetViewSet):
    serializer_class = StatusOutBudgetSerializer


class ExecAmountToBudgetViewSet(viewsets.ModelViewSet):
    serializer_class = ExecAmountToBudget
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)

    def get_queryset(self):
        date = self.request.query_params.get('date')
        date = date if date else TODAY
        month_first = datetime(datetime.strptime(date, '%Y-%m-%d').year,
                               datetime.strptime(date, '%Y-%m-%d').month,
                               1).strftime('%Y-%m-%d')

        queryset = ProjectCashBook.objects.all() \
            .order_by('project_account_d2') \
            .filter(is_separate=False,
                    project_account_d2__d1__gte=6,
                    project_account_d2__d1__lte=10,
                    bank_account__directpay=False,
                    deal_date__lte=date)

        return queryset.annotate(acc_d2=F('project_account_d2')) \
            .values('acc_d2') \
            .annotate(all_sum=Sum('outlay'),
                      month_sum=Sum(Case(
                          When(deal_date__gte=month_first, then=F('outlay')),
                          default=0
                      )))


class UnitFloorTypeViewSet(viewsets.ModelViewSet):
    queryset = UnitFloorType.objects.all()
    serializer_class = UnitFloorTypeSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)
    search_fields = ('alias_name',)


class KeyUnitListFilterSet(FilterSet):
    available = BooleanFilter(field_name='contract', lookup_expr='isnull', label='계약가능유닛')

    class Meta:
        model = KeyUnit
        fields = ('project', 'unit_type', 'contract', 'available')


class KeyUnitViewSet(viewsets.ModelViewSet):
    queryset = KeyUnit.objects.all()
    serializer_class = KeyUnitSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_class = KeyUnitListFilterSet


class BuildingUnitViewSet(viewsets.ModelViewSet):
    queryset = BuildingUnit.objects.all()
    serializer_class = BuildingUnitSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)
    search_fields = ('name',)


class HouseUnitViewSet(viewsets.ModelViewSet):
    queryset = HouseUnit.objects.all()
    serializer_class = HouseUnitSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project', 'building_unit')
    search_fields = ('hold_reason',)


class AvailableHouseUnitViewSet(HouseUnitViewSet):

    def get_queryset(self):
        houseunit = HouseUnit.objects.all()
        queryset = houseunit

        project = self.request.query_params.get('project', None)
        unit_type = self.request.query_params.get('unit_type', None)

        if project and unit_type:
            queryset = houseunit.filter(project=project, unit_type=unit_type, key_unit__isnull=True)

        contract = self.request.query_params.get('contract', None)
        if contract is not None:
            queryset = houseunit.filter(
                Q(project=project, unit_type=unit_type, key_unit__isnull=True) |
                Q(key_unit__contract=contract))
        return queryset


class AllHouseUnitViewSet(HouseUnitViewSet):
    serializer_class = AllHouseUnitSerializer
    pagination_class = PageNumberPaginationThreeThousand


class TotalSiteAreaViewSet(viewsets.ModelViewSet):
    serializer_class = TotalSiteAreaSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)

    def get_queryset(self):
        return Site.objects.values('project') \
            .annotate(official=Sum('official_area'),
                      returned=Sum('returned_area'))


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)
    search_fields = ('district', 'lot_number', 'site_purpose', 'owners__owner')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllSiteViewSet(SiteViewSet):
    serializer_class = AllSiteSerializer
    pagination_class = PageNumberPaginationFiveHundred


class TotalOwnerAreaViewSet(viewsets.ModelViewSet):
    serializer_class = TotalOwnerAreaSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)

    def get_queryset(self):
        return Site.objects.values('project') \
            .annotate(owned_area=Sum('siteownshiprelationship__owned_area'))


class SiteOwnerViewSet(viewsets.ModelViewSet):
    queryset = SiteOwner.objects.all()
    serializer_class = SiteOwnerSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project', 'own_sort')
    search_fields = ('owner', 'phone1', 'phone2', 'sites__lot_number', 'counsel_record')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllOwnerViewSet(SiteOwnerViewSet):
    queryset = SiteOwner.objects.all().order_by('id')
    serializer_class = AllOwnerSerializer
    pagination_class = PageNumberPaginationFiveHundred
    filterset_fields = ('project',)


class SiteRelationViewSet(viewsets.ModelViewSet):
    queryset = SiteOwnshipRelationship.objects.all()
    serializer_class = SiteOwnshipRelationshipSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class TotalContractedAreaViewSet(viewsets.ModelViewSet):
    serializer_class = TotalContractedAreaSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project',)

    def get_queryset(self):
        return SiteContract.objects.values('project') \
            .annotate(contracted_area=Sum('contract_area'))


class SiteContractViewSet(viewsets.ModelViewSet):
    queryset = SiteContract.objects.all()
    serializer_class = SiteContractSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('project', 'owner__own_sort')
    search_fields = ('owner__owner', 'owner__phone1', 'acc_bank', 'acc_owner', 'note')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
