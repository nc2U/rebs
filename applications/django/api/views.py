from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import FilterSet
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter

from .permission import *
from .pagination import *
from .serializers import *

from accounts.models import User, Profile, Todo
from company.models import Company, Department, Staff
from project.models import (Project, UnitType, UnitFloorType,
                            ContractUnit, UnitNumber, ProjectBudget,
                            Site, SiteOwner, SiteOwnshipRelationship, SiteContract)
from rebs.models import (AccountSubD1, AccountSubD2, AccountSubD3,
                         ProjectAccountD1, ProjectAccountD2, WiseSaying)
from cash.models import (BankCode, CompanyBankAccount, ProjectBankAccount,
                         CashBook, ProjectCashBook, SalesPriceByGT,
                         InstallmentPaymentOrder, DownPayment, OverDueRule)
from contract.models import (OrderGroup, Contract, Contractor,
                             ContractorAddress, ContractorContact, ContractorRelease)
from notice.models import SalesBillIssue
from document.models import Group, Board, Category, LawsuitCase, Post, Image, Link, File, Comment, Tag


class ApiIndex(generics.GenericAPIView):
    name = 'api-index'
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        api = 'api:'
        return Response({
            'user': reverse(api + UserList.name, request=request),
            'profile': reverse(api + ProfileList.name, request=request),
            'todo': reverse(api + TodoList.name, request=request),
            'company': reverse(api + CompanyList.name, request=request),
            'department': reverse(api + DepartmentList.name, request=request),
            'staff': reverse(api + StaffList.name, request=request),
            'project': reverse(api + ProjectList.name, request=request),
            'unit-type': reverse(api + UnitTypeList.name, request=request),
            'contract-unit': reverse(api + ContractUnitList.name, request=request),
            'unit-number': reverse(api + UnitNumberList.name, request=request),
            'budget': reverse(api + ProjectBudgetList.name, request=request),
            'site': reverse(api + SiteList.name, request=request),
            'site-owner': reverse(api + SiteOwnerList.name, request=request),
            'relation': reverse(api + RelationList.name, request=request),
            'site-contract': reverse(api + SiteContractList.name, request=request),
            'account-depth1': reverse(api + AccountSubD1List.name, request=request),
            'account-depth2': reverse(api + AccountSubD2List.name, request=request),
            'account-depth3': reverse(api + AccountSubD3List.name, request=request),
            'project-acc-d1': reverse(api + ProjectAccountD1List.name, request=request),
            'project-acc-d2': reverse(api + ProjectAccountD2List.name, request=request),
            'bank-code': reverse(api + BankCodeList.name, request=request),
            'com-bank': reverse(api + ComBankAccountList.name, request=request),
            'cashbook': reverse(api + CashBookList.name, request=request),
            'project-bank': reverse(api + ProjectBankAccountList.name, request=request),
            'project-cashbook': reverse(api + ProjectCashBookList.name, request=request),
            'price': reverse(api + SalesPriceList.name, request=request),
            'install-order': reverse(api + InstallmentOrderList.name, request=request),
            'down-payment': reverse(api + DownPaymentList.name, request=request),
            'over-due-rule': reverse(api + OverDueRuleList.name, request=request),
            'order-group': reverse(api + OrderGroupList.name, request=request),
            'contract': reverse(api + ContractList.name, request=request),
            'contractor': reverse(api + ContractorList.name, request=request),
            'contractor-address': reverse(api + ContAddressList.name, request=request),
            'contractor-contact': reverse(api + ContContactList.name, request=request),
            'contractor-release': reverse(api + ContReleaseList.name, request=request),
            'sales-bill-issue': reverse(api + BillIssueList.name, request=request),
            'group': reverse(api + GroupList.name, request=request),
            'board': reverse(api + BoardList.name, request=request),
            'category': reverse(api + CategoryList.name, request=request),
            'suitcase': reverse(api + LawSuitCaseList.name, request=request),
            'post': reverse(api + PostList.name, request=request),
            'image': reverse(api + ImageList.name, request=request),
            'link': reverse(api + LinkList.name, request=request),
            'file': reverse(api + FileList.name, request=request),
            'comment': reverse(api + CommentList.name, request=request),
            'tag': reverse(api + TagList.name, request=request),
            'wise-say': reverse(api + WiseSayList.name, request=request),
        })


# User --------------------------------------------------------------------------
class UserList(generics.ListCreateAPIView):
    name = 'user-list'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'user-detail'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnSelfOrReadOnly)


# Profile --------------------------------------------------------------------------
class ProfileList(generics.ListCreateAPIView):
    name = 'profile-list'
    queryset = Profile.objects.all()
    serializer_class = UserInProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'profile-detail'
    queryset = Profile.objects.all()
    serializer_class = UserInProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly)


# T o d o --------------------------------------------------------------------------
class TodoList(generics.ListCreateAPIView):
    name = 'todo-list'
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = PageNumberPaginationForTodoList
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly)
    filter_fields = ('user', 'soft_deleted')
    search_fields = ('title',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'todo-detail'
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly)


# Company --------------------------------------------------------------------------
class CompanyList(generics.ListCreateAPIView):
    name = 'company-list'
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'company-detail'
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class DepartmentList(generics.ListCreateAPIView):
    name = 'depart-list'
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'depart-detail'
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class StaffList(generics.ListCreateAPIView):
    name = 'staff-list'
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class StaffDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'staff-detail'
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


# Project --------------------------------------------------------------------------
class ProjectList(generics.ListCreateAPIView):
    name = 'project-list'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'project-detail'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class UnitTypeList(generics.ListCreateAPIView):
    name = 'unittype-list'
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class UnitTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'unittype-detail'
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContractUnitList(generics.ListCreateAPIView):
    name = 'contractunit-list'
    queryset = ContractUnit.objects.all()
    serializer_class = ContractUnitSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContractUnitDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'contractunit-detail'
    queryset = ContractUnit.objects.all()
    serializer_class = ContractUnitSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class UnitNumberList(generics.ListCreateAPIView):
    name = 'unitnumber-list'
    queryset = UnitNumber.objects.all()
    serializer_class = UnitNumberSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class UnitNumberDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'unitnumber-detail'
    queryset = UnitNumber.objects.all()
    serializer_class = UnitNumberSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ProjectBudgetList(generics.ListCreateAPIView):
    name = 'projectbudget-list'
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ProjectBudgetDetail(generics.ListCreateAPIView):
    name = 'projectbudget-detail'
    queryset = ProjectBudget.objects.all()
    serializer_class = ProjectBudgetSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class SiteList(generics.ListCreateAPIView):
    name = 'site-list'
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class SiteDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'site-detail'
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class SiteOwnerList(generics.ListCreateAPIView):
    name = 'siteowner-list'
    queryset = SiteOwner.objects.all()
    serializer_class = SiteOwnerSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class SiteOwnerDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'siteowner-detail'
    queryset = SiteOwner.objects.all()
    serializer_class = SiteOwnerSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class RelationList(generics.ListCreateAPIView):
    name = 'relation-list'
    queryset = SiteOwnshipRelationship.objects.all()
    serializer_class = SiteOwnshipRelationSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class RelationDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'relation-detail'
    queryset = SiteOwnshipRelationship.objects.all()
    serializer_class = SiteOwnshipRelationSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class SiteContractList(generics.ListCreateAPIView):
    name = 'sitecontract-list'
    queryset = SiteContract.objects.all()
    serializer_class = SiteContractSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class SiteContractDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'sitecontract-detail'
    queryset = SiteContract.objects.all()
    serializer_class = SiteContractSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class AccountSubD1List(generics.ListAPIView):
    name = 'acc_d1-list'
    queryset = AccountSubD1.objects.all()
    serializer_class = AccountSubD1Serializer


class AccountSubD1Detail(generics.RetrieveAPIView):
    name = 'acc_d1-detail'
    queryset = AccountSubD1.objects.all()
    serializer_class = AccountSubD1Serializer


class AccountSubD2List(generics.ListAPIView):
    name = 'acc_d2-list'
    queryset = AccountSubD2.objects.all()
    serializer_class = AccountSubD2Serializer


class AccountSubD2Detail(generics.RetrieveAPIView):
    name = 'acc_d2-detail'
    queryset = AccountSubD2.objects.all()
    serializer_class = AccountSubD2Serializer


class AccountSubD3List(generics.ListAPIView):
    name = 'acc_d3-list'
    queryset = AccountSubD3.objects.all()
    serializer_class = AccountSubD3Serializer


class AccountSubD3Detail(generics.RetrieveAPIView):
    name = 'acc_d3-detail'
    queryset = AccountSubD3.objects.all()
    serializer_class = AccountSubD3Serializer


class ProjectAccountD1List(generics.ListAPIView):
    name = 'project_acc_d1-list'
    queryset = ProjectAccountD1.objects.all()
    serializer_class = ProjectAccountD1Serializer


class ProjectAccountD1Detail(generics.RetrieveAPIView):
    name = 'project_acc_d1-detail'
    queryset = ProjectAccountD1.objects.all()
    serializer_class = ProjectAccountD1Serializer


class ProjectAccountD2List(generics.ListAPIView):
    name = 'project_acc_d2-list'
    queryset = ProjectAccountD2.objects.all()
    serializer_class = ProjectAccountD2Serializer


class ProjectAccountD2Detail(generics.RetrieveAPIView):
    name = 'project_acc_d2-detail'
    queryset = ProjectAccountD2.objects.all()
    serializer_class = ProjectAccountD2Serializer


class BankCodeList(generics.ListAPIView):
    name = 'bankcode-list'
    queryset = BankCode.objects.all()
    serializer_class = BankCodeSerializer


class BankCodeDetail(generics.ListAPIView):
    name = 'bankcode-detail'
    queryset = BankCode.objects.all()
    serializer_class = BankCodeSerializer


class ComBankAccountList(generics.ListCreateAPIView):
    name = 'com_bank-list'
    queryset = CompanyBankAccount.objects.all()
    serializer_class = CompanyBankAccountSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ComBankAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'com_bank-detail'
    queryset = CompanyBankAccount.objects.all()
    serializer_class = CompanyBankAccountSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CashBookList(generics.ListCreateAPIView):
    name = 'cashbook-list'
    queryset = CashBook.objects.all()
    serializer_class = CashBookSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CashBookDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'cashbook-detail'
    queryset = CashBook.objects.all()
    serializer_class = CashBookSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ProjectBankAccountList(generics.ListCreateAPIView):
    name = 'project_bank-list'
    queryset = ProjectBankAccount.objects.all()
    serializer_class = ProjectBankAccountSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ProjectBankAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'project_bank-detail'
    queryset = ProjectBankAccount.objects.all()
    serializer_class = ProjectBankAccountSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ProjectCashBookList(generics.ListCreateAPIView):
    name = 'project_cashbook-list'
    queryset = ProjectCashBook.objects.all()
    serializer_class = ProjectCashBookSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectCashBookDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'project_cashbook-detail'
    queryset = ProjectCashBook.objects.all()
    serializer_class = ProjectCashBookSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class SalesPriceList(generics.ListCreateAPIView):
    name = 'price-list'
    queryset = SalesPriceByGT.objects.all()
    serializer_class = SalesPriceSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class SalesPriceDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'price-detail'
    queryset = SalesPriceByGT.objects.all()
    serializer_class = SalesPriceSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class InstallmentOrderList(generics.ListCreateAPIView):
    name = 'install_order-list'
    queryset = InstallmentPaymentOrder.objects.all()
    serializer_class = InstallmentOrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class InstallmentOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'install_order-detail'
    queryset = InstallmentPaymentOrder.objects.all()
    serializer_class = InstallmentOrderSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class DownPaymentList(generics.ListCreateAPIView):
    name = 'downpay-list'
    queryset = DownPayment.objects.all()
    serializer_class = DownPaymentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class DownPaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'downpay-detail'
    queryset = DownPayment.objects.all()
    serializer_class = DownPaymentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class OverDueRuleList(generics.ListCreateAPIView):
    name = 'over_due_rule-list'
    queryset = OverDueRule.objects.all()
    serializer_class = OverDueRuleSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class OverDueRuleDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'over_due_rule-detail'
    queryset = OverDueRule.objects.all()
    serializer_class = OverDueRuleSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class OrderGroupList(generics.ListCreateAPIView):
    name = 'order_group-list'
    queryset = OrderGroup.objects.all()
    serializer_class = OrderGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class OrderGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'order_group-detail'
    queryset = OrderGroup.objects.all()
    serializer_class = OrderGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContractList(generics.ListCreateAPIView):
    name = 'contract-list'
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'contract-detail'
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ContractorList(generics.ListCreateAPIView):
    name = 'contractor-list'
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

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
    queryset = ContractorRelease.objects.all()
    serializer_class = ContractorReleaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContReleaseDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'release-detail'
    queryset = ContractorRelease.objects.all()
    serializer_class = ContractorReleaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BillIssueList(generics.ListCreateAPIView):
    name = 'bill_issue-list'
    queryset = SalesBillIssue.objects.all()
    serializer_class = SallesBillIssueSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BillIssueDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'bill_issue-detail'
    queryset = SalesBillIssue.objects.all()
    serializer_class = SallesBillIssueSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class GroupList(generics.ListCreateAPIView):
    name = 'group-list'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'group-detail'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BoardList(generics.ListCreateAPIView):
    name = 'board-list'
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'board-detail'
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CategoryList(generics.ListCreateAPIView):
    name = 'category-list'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'category-detail'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class LawSuitCaseList(generics.ListCreateAPIView):
    name = 'suitcase-list'
    queryset = LawsuitCase.objects.all()
    serializer_class = LawSuitCaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LawSuitCaseDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'suitcase-detail'
    queryset = LawsuitCase.objects.all()
    serializer_class = LawSuitCaseSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class PostList(generics.ListCreateAPIView):
    name = 'post-list'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'post-detail'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ImageList(generics.ListCreateAPIView):
    name = 'image-list'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'image-detail'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class LinkList(generics.ListCreateAPIView):
    name = 'link-list'
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'link-detail'
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class FileList(generics.ListCreateAPIView):
    name = 'file-list'
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'file-detail'
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class CommentList(generics.ListCreateAPIView):
    name = 'comment-list'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'comment-detail'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class TagList(generics.ListCreateAPIView):
    name = 'tag-list'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'tag-detail'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


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
