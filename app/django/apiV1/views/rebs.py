from rest_framework import viewsets

from ..permission import *
from ..pagination import *
from ..serializers.rebs import *

from rebs.models import (AccountSort, AccountSubD1, AccountSubD2, AccountSubD3,
                         ProjectAccountSort, ProjectAccountD1, ProjectAccountD2,
                         CalendarSchedule, WiseSaying)


# Rebs --------------------------------------------------------------------------
class CalendarScheduleViewSet(viewsets.ModelViewSet):
    queryset = CalendarSchedule.objects.all()
    serializer_class = CalendarScheduleSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
    pagination_class = PageNumberPaginationOneHundred
    search_fields = ('start_date', 'start_time', 'end_date', 'end_time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountSortViewSet(viewsets.ModelViewSet):
    queryset = AccountSort.objects.all()
    serializer_class = AccountSortSerializer


class AccountSubD1ViewSet(viewsets.ModelViewSet):
    queryset = AccountSubD1.objects.all()
    serializer_class = AccountSubD1Serializer
    filterset_fields = ('accountsort',)


class AccountSubD2ViewSet(viewsets.ModelViewSet):
    queryset = AccountSubD2.objects.all()
    serializer_class = AccountSubD2Serializer
    pagination_class = PageNumberPaginationTwenty
    filterset_fields = ('d1__accountsort', 'd1')


class AccountSubD3ViewSet(viewsets.ModelViewSet):
    queryset = AccountSubD3.objects.all()
    serializer_class = AccountSubD3Serializer
    pagination_class = PageNumberPaginationTwoHundred
    filterset_fields = ('d2__d1__accountsort', 'd2__d1', 'd2')


class ProjectAccountSortViewSet(viewsets.ModelViewSet):
    queryset = ProjectAccountSort.objects.all()
    serializer_class = AccountSortSerializer


class ProjectAccountD1ViewSet(viewsets.ModelViewSet):
    queryset = ProjectAccountD1.objects.all()
    pagination_class = PageNumberPaginationTwenty
    serializer_class = ProjectAccountD1Serializer
    filterset_fields = ('projectaccountsort', 'acc')


class ProjectAccountD2ViewSet(viewsets.ModelViewSet):
    queryset = ProjectAccountD2.objects.all()
    pagination_class = PageNumberPaginationOneHundred
    serializer_class = ProjectAccountD2Serializer
    filterset_fields = ('d1', 'd1__projectaccountsort')


class WiseSayViewSet(viewsets.ModelViewSet):
    queryset = WiseSaying.objects.all()
    serializer_class = WiseSaySerializer
    permissions_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
