from rest_framework import generics, viewsets

from ..permission import *
from ..serializers.notice import *

from notice.models import SalesBillIssue


class BillIssueList(generics.ListCreateAPIView):
    name = 'bill_issue-list'
    queryset = SalesBillIssue.objects.all()
    serializer_class = SallesBillIssueSerializer
    filter_fields = ('project',)
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BillIssueDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'bill_issue-detail'
    queryset = SalesBillIssue.objects.all()
    serializer_class = SallesBillIssueSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
