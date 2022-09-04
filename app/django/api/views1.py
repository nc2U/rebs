from datetime import datetime
from django.db.models import Sum, Count, F, Q, Case, When
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import FilterSet
from django_filters import ChoiceFilter, ModelChoiceFilter, DateFilter, BooleanFilter

from .permission import *
from .pagination import *
# from .serializers1 import *

from project.models import (Project, UnitType, UnitFloorType,
                            KeyUnit, BuildingUnit, HouseUnit, ProjectBudget,
                            Site, SiteOwner, SiteOwnshipRelationship, SiteContract)

from cash.models import (BankCode, CompanyBankAccount, ProjectBankAccount,
                         CashBook, ProjectCashBook, SalesPriceByGT,
                         InstallmentPaymentOrder, DownPayment, OverDueRule)
from contract.models import (OrderGroup, Contract, Contractor,
                             ContractorAddress, ContractorContact, ContractorRelease)
from notice.models import SalesBillIssue
from document.models import Group, Board, Category, LawsuitCase, Post, Image, Link, File, Comment, Tag

from .views.rebs import *
from .views.project import *
from .views.cash import *
from .views.contract import *


class ApiIndex(generics.GenericAPIView):
    name = 'api-index'
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        api = 'api:'
        return Response({
            # accounts
            'user': reverse(api + 'user-list', request=request),
            'profile': reverse(api + 'profile-list', request=request),
            'todo': reverse(api + 'todo-list', request=request),
            # company
            'company': reverse(api + 'company-list', request=request),
            'logo': reverse(api + 'logo-list', request=request),
            'department': reverse(api + 'depart-list', request=request),
            'position': reverse(api + 'position-list', request=request),
            'staff': reverse(api + 'staff-list', request=request),
            # rebs
            'schedule': reverse(api + 'schedule-list', request=request),
            'account-sort': reverse(api + AccountSortList.name, request=request),
            'account-depth1': reverse(api + AccountSubD1List.name, request=request),
            'account-depth2': reverse(api + AccountSubD2List.name, request=request),
            'account-depth3': reverse(api + AccountSubD3List.name, request=request),
            'project-acc-sort': reverse(api + ProjectAccountSortList.name, request=request),
            'project-acc-d1': reverse(api + ProjectAccountD1List.name, request=request),
            'project-acc-d2': reverse(api + ProjectAccountD2List.name, request=request),
            # project
            'project': reverse(api + 'project-list', request=request),
            'type': reverse(api + 'unittype-list', request=request),
            'floor': reverse(api + 'floortype-list', request=request),
            'key-unit': reverse(api + 'key_unit-list', request=request),
            'bldg-unit': reverse(api + 'bldg-list', request=request),
            'house-unit': reverse(api + HouseUnitList.name, request=request),
            'available-house-unit': reverse(api + AvailableHouseUnitList.name, request=request),
            'all-house-unit': reverse(api + AllHouseUnitList.name, request=request),
            'budget': reverse(api + ProjectBudgetList.name, request=request),
            'exec-amount-budget': reverse(api + ExecAmountToBudgetList.name, request=request),
            'all-site': reverse(api + AllSiteList.name, request=request),
            'sites-total': reverse(api + TotalSiteArea.name, request=request),
            'site': reverse(api + 'site-list', request=request),
            'all-owner': reverse(api + AllOwnerList.name, request=request),
            'owners-total': reverse(api + TotalOwnerArea.name, request=request),
            'site-owner': reverse(api + 'siteowner-list', request=request),
            'site-relation': reverse(api + 'relation-list', request=request),
            'conts-total': reverse(api + TotalContractedArea.name, request=request),
            'site-contract': reverse(api + 'sitecontract-list', request=request),
            # cash
            'bank-code': reverse(api + BankCodeList.name, request=request),
            'com-bank': reverse(api + 'com_bank-list', request=request),
            'balance-by-acc': reverse(api + BalanceByAccountList.name, request=request),
            'cashbook': reverse(api + CashBookList.name, request=request),
            'date-cashbook': reverse(api + DateCashBookList.name, request=request),
            'project-bank': reverse(api + ProjectBankAccountList.name, request=request),
            'pr-balance-by-acc': reverse(api + PrBalanceByAccountList.name, request=request),
            'pr-date-cashbook': reverse(api + ProjectDateCashBookList.name, request=request),
            'project-cashbook': reverse(api + ProjectCashBookList.name, request=request),
            'project-imprest': reverse(api + ProjectImprestList.name, request=request),
            'payment-list': reverse(api + PaymentList.name, request=request),
            'all-payment-list': reverse(api + AllPaymentList.name, request=request),
            'payment-sum': reverse(api + PaymentSummary.name, request=request),
            'cont-count': reverse(api + NumContractByType.name, request=request),
            'price': reverse(api + SalesPriceList.name, request=request),
            'pay-order': reverse(api + InstallmentOrderList.name, request=request),
            'down-payment': reverse(api + DownPaymentList.name, request=request),
            # 'over-due-rule': reverse(api + OverDueRuleList.name, request=request),
            # contract
            'order-group': reverse(api + OrderGroupList.name, request=request),
            'contract': reverse(api + ContractList.name, request=request),
            'contract-custom-list': reverse(api + ContractCustomList.name, request=request),
            'subs-sum': reverse(api + SubsSummaryList.name, request=request),
            'cont-sum': reverse(api + ContSummaryList.name, request=request),
            'contractor': reverse(api + ContractorList.name, request=request),
            'contractor-address': reverse(api + ContAddressList.name, request=request),
            'contractor-contact': reverse(api + ContContactList.name, request=request),
            'contractor-release': reverse(api + ContReleaseList.name, request=request),
            
            # 'sales-bill-issue': reverse(api + BillIssueList.name, request=request),
            # # 'group': reverse(api + GroupList.name, request=request),
            # # 'board': reverse(api + BoardList.name, request=request),
            # # 'category': reverse(api + CategoryList.name, request=request),
            # # 'suitcase': reverse(api + LawSuitCaseList.name, request=request),
            # # 'post': reverse(api + PostList.name, request=request),
            # # 'image': reverse(api + ImageList.name, request=request),
            # # 'link': reverse(api + LinkList.name, request=request),
            # # 'file': reverse(api + FileList.name, request=request),
            # # 'comment': reverse(api + CommentList.name, request=request),
            # # 'tag': reverse(api + TagList.name, request=request),
            # 'wise-say': reverse(api + WiseSayList.name, request=request),
        })

# class BillIssueList(generics.ListCreateAPIView):
#     name = 'bill_issue-list'
#     queryset = SalesBillIssue.objects.all()
#     serializer_class = SallesBillIssueSerializer
#     filter_fields = ('project',)
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class BillIssueDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'bill_issue-detail'
#     queryset = SalesBillIssue.objects.all()
#     serializer_class = SallesBillIssueSerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # # Document --------------------------------------------------------------------------
# # class GroupList(generics.ListCreateAPIView):
# #     name = 'group-list'
# #     queryset = Group.objects.all()
# #     serializer_class = GroupSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #
# # class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'group-detail'
# #     queryset = Group.objects.all()
# #     serializer_class = GroupSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #
# # class BoardList(generics.ListCreateAPIView):
# #     name = 'board-list'
# #     queryset = Board.objects.all()
# #     serializer_class = BoardSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #
# # class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'board-detail'
# #     queryset = Board.objects.all()
# #     serializer_class = BoardSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # class CategoryList(generics.ListCreateAPIView):
# #     name = 'category-list'
# #     queryset = Category.objects.all()
# #     serializer_class = CategorySerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #
# # class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'category-detail'
# #     queryset = Category.objects.all()
# #     serializer_class = CategorySerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # class LawSuitCaseList(generics.ListCreateAPIView):
# #     name = 'suitcase-list'
# #     queryset = LawsuitCase.objects.all()
# #     serializer_class = LawSuitCaseSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #     def perform_create(self, serializer):
# #         serializer.save(user=self.request.user)
# #
# #
# # class LawSuitCaseDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'suitcase-detail'
# #     queryset = LawsuitCase.objects.all()
# #     serializer_class = LawSuitCaseSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # class PostList(generics.ListCreateAPIView):
# #     name = 'post-list'
# #     queryset = Post.objects.all()
# #     serializer_class = PostSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #     def perform_create(self, serializer):
# #         serializer.save(user=self.request.user)
# #
# #
# # class PostDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'post-detail'
# #     queryset = Post.objects.all()
# #     serializer_class = PostSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # class ImageList(generics.ListCreateAPIView):
# #     name = 'image-list'
# #     queryset = Image.objects.all()
# #     serializer_class = ImageSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'image-detail'
# #     queryset = Image.objects.all()
# #     serializer_class = ImageSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # class LinkList(generics.ListCreateAPIView):
# #     name = 'link-list'
# #     queryset = Link.objects.all()
# #     serializer_class = LinkSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #
# # class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'link-detail'
# #     queryset = Link.objects.all()
# #     serializer_class = LinkSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # class FileList(generics.ListCreateAPIView):
# #     name = 'file-list'
# #     queryset = File.objects.all()
# #     serializer_class = FileSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #
# # class FileDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'file-detail'
# #     queryset = File.objects.all()
# #     serializer_class = FileSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # class CommentList(generics.ListCreateAPIView):
# #     name = 'comment-list'
# #     queryset = Comment.objects.all()
# #     serializer_class = CommentSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #     def perform_create(self, serializer):
# #         serializer.save(user=self.request.user)
# #
# #
# # class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'comment-detail'
# #     queryset = Comment.objects.all()
# #     serializer_class = CommentSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # class TagList(generics.ListCreateAPIView):
# #     name = 'tag-list'
# #     queryset = Tag.objects.all()
# #     serializer_class = TagSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
# #
# #
# # class TagDetail(generics.RetrieveUpdateDestroyAPIView):
# #     name = 'tag-detail'
# #     queryset = Tag.objects.all()
# #     serializer_class = TagSerializer
# #     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# # Etc --------------------------------------------------------------------------
# class WiseSayList(generics.ListCreateAPIView):
#     name = 'wise-say-list'
#     queryset = WiseSaying.objects.all()
#     serializer_class = WiseSaySerializer
#     permissions_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
#
#
# class WiseSayDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'wise-say-detail'
#     queryset = WiseSaying.objects.all()
#     serializer_class = WiseSaySerializer
#     permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)
