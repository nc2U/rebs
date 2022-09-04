from rest_framework import generics, viewsets

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


class AccountSortList(generics.ListAPIView):
    name = 'acc_sort-list'
    queryset = AccountSort.objects.all()
    serializer_class = AccountSortSerializer


class AccountSubD1List(generics.ListAPIView):
    name = 'acc_d1-list'
    queryset = AccountSubD1.objects.all()
    serializer_class = AccountSubD1Serializer
    filter_fields = ('accountsort',)


class AccountSubD2List(generics.ListAPIView):
    name = 'acc_d2-list'
    queryset = AccountSubD2.objects.all()
    serializer_class = AccountSubD2Serializer
    pagination_class = PageNumberPaginationTwenty
    filter_fields = ('d1__accountsort', 'd1')


class AccountSubD3List(generics.ListAPIView):
    name = 'acc_d3-list'
    queryset = AccountSubD3.objects.all()
    serializer_class = AccountSubD3Serializer
    pagination_class = PageNumberPaginationTwoHundred
    filter_fields = ('d2__d1__accountsort', 'd2__d1', 'd2')


class ProjectAccountSortList(generics.ListAPIView):
    name = 'pro-acc_sort-list'
    queryset = ProjectAccountSort.objects.all()
    serializer_class = AccountSortSerializer


class ProjectAccountD1List(generics.ListAPIView):
    name = 'project_acc_d1-list'
    queryset = ProjectAccountD1.objects.all()
    pagination_class = PageNumberPaginationTwenty
    serializer_class = ProjectAccountD1Serializer
    filter_fields = ('projectaccountsort',)


class ProjectAccountD2List(generics.ListAPIView):
    name = 'project_acc_d2-list'
    queryset = ProjectAccountD2.objects.all()
    pagination_class = PageNumberPaginationOneHundred
    serializer_class = ProjectAccountD2Serializer
    filter_fields = ('d1', 'd1__projectaccountsort')


class WiseSayList(generics.ListCreateAPIView):
    name = 'wise-say-list'
    queryset = WiseSaying.objects.all()
    serializer_class = WiseSaySerializer
    permissions_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class WiseSayDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'wise-say-detail'
    queryset = WiseSaying.objects.all()
    serializer_class = WiseSaySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
