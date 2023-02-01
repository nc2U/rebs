from rest_framework import viewsets

from ..permission import *
from ..pagination import *
from ..serializers.company import *

from company.models import Company, Logo, Department, JobGrade, Position, DutyTitle, Staff


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
    filterset_fields = ('company', 'upper_depart')
    search_fields = ('name', 'task')


class AllDepartsViewSet(DepartmentViewSet):
    pagination_class = PageNumberPaginationOneHundred
    filterset_fields = ('company',)


class JobGradeViewSet(viewsets.ModelViewSet):
    queryset = JobGrade.objects.all()
    serializer_class = JobGradeSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('company',)
    search_fields = ('grade', 'promotion_period', 'criteria_new')


class AllGradesViewSet(JobGradeViewSet):
    pagination_class = PageNumberPaginationOneHundred
    filterset_fields = ('company',)


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('company',)
    search_fields = ('position',)


class DutyTitleViewSet(viewsets.ModelViewSet):
    queryset = DutyTitle.objects.all()
    serializer_class = DutyTitleSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('company',)
    search_fields = ('title',)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    filterset_fields = ('company', 'sort', 'department', 'grade', 'position', 'duty', 'status')
    search_fields = ('name', 'id_number', 'personal_phone', 'email')
