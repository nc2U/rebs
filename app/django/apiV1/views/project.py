from datetime import datetime
from django.db.models import Sum, F, Case, When
from rest_framework import viewsets

from ..permission import *
from ..pagination import *
from ..serializers.project import *

from project.models import (Project, ProjectIncBudget, ProjectOutBudget,
                            Site, SiteOwner, SiteOwnshipRelationship, SiteContract)

from cash.models import BankCode, CompanyBankAccount, ProjectBankAccount, CashBook, ProjectCashBook

TODAY = datetime.today().strftime('%Y-%m-%d')


# Project --------------------------------------------------------------------------
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


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
            .order_by('project_account_d3') \
            .filter(is_separate=False,
                    project_account_d3__d2__gte=6,
                    project_account_d3__d2__lte=10,
                    bank_account__directpay=False,
                    deal_date__lte=date)

        return queryset.annotate(acc_d3=F('project_account_d3')) \
            .values('acc_d3') \
            .annotate(all_sum=Sum('outlay'),
                      month_sum=Sum(Case(
                          When(deal_date__gte=month_first, then=F('outlay')),
                          default=0
                      )))


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
