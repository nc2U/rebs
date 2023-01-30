from rest_framework import viewsets

from ..permission import *
from ..pagination import *
from ..serializers.company import *

from company.models import Company, Logo, Department, JobRank, Staff


# Company --------------------------------------------------------------------------
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class LogoViewSet(viewsets.ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class AllDepartsViewSet(DepartmentViewSet):
    pagination_class = PageNumberPaginationOneHundred


class JobRankViewSet(viewsets.ModelViewSet):
    queryset = JobRank.objects.all()
    serializer_class = JobRankSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class AllRanksViewSet(JobRankViewSet):
    pagination_class = PageNumberPaginationOneHundred


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
