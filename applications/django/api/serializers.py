from rest_framework import serializers

from accounts.models import User, StaffAuth, Todo
from book.models import Book, Subject
from company.models import Company, Department, Position, Staff
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


class UserInStaffAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAuth
        fields = (
            'id', 'company', 'is_staff', 'assigned_project', 'allowed_projects', 'contract', 'payment', 'notice',
            'project_cash',
            'project_docs',
            'project', 'company_cash', 'company_docs', 'human_resource', 'company_settings', 'auth_manage')


class UserInTodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'completed', 'soft_deleted')


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:user-detail')
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='변경할 필요가 없으면 비워 두십시오.',
        style={'input_type': 'password', 'placeholder': '비밀번호'}
    )
    staffauth = UserInStaffAuthSerializer()
    todos = UserInTodosSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id', 'url', 'email', 'username', 'is_active', 'is_superuser', 'date_joined', 'password', 'staffauth',
            'todos')

    def save(self):
        instance = User(email=self.validated_data['email'],
                        username=self.validated_data['username'])
        password = self.validated_data['password']
        instance.set_password(password)
        instance.save()
        self.instance = instance
        return self.instance


class BookInSubjectsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username', required=False)

    class Meta:
        model = Subject
        fields = ('id', 'user', 'book', 'seq', 'title', 'level', 'content', 'created_at', 'updated_at')


class BookSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:book-detail")
    user = serializers.ReadOnlyField(source='user.username', required=False)
    subjects = BookInSubjectsSerializer(many=True)

    class Meta:
        model = Book
        fields = (
            'id', 'url', 'user', 'title', 'disclosure', 'author', 'translator', 'publisher', 'pub_date', 'description',
            'created_at', 'updated_at', 'subjects')


class CompanyInDepartsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:depart-detail')

    class Meta:
        model = Department
        fields = ('id', 'url', 'upper_depart', 'name', 'task')


class CompanyInPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'rank', 'title', 'description')


class CompanySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:company-detail')
    departments = CompanyInDepartsSerializer(many=True, read_only=True)
    positions = CompanyInPositionsSerializer(many=True)

    class Meta:
        model = Company
        fields = ('id', 'url', 'name', 'ceo', 'tax_number', 'org_number',
                  'business_cond', 'business_even', 'es_date', 'op_date', 'zipcode',
                  'address1', 'address2', 'address3', 'departments', 'positions')


class StaffInDepartmentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:staff-detail')

    class Meta:
        model = Staff
        fields = ('id', 'url', 'position', 'name')


class DepartmentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:depart-detail')
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='name')
    staffs = StaffInDepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('id', 'url', 'company', 'name', 'task', 'staffs')


class StaffSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:staff-detail')
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name')
    gender = serializers.ChoiceField(choices=Staff.GENDER_CHOICES)
    gender_desc = serializers.CharField(source='get_gender_display', read_only=True)
    status = serializers.ChoiceField(choices=Staff.STATUS_CHOICES)
    status_desc = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Staff
        fields = ('id', 'url', 'department', 'position', 'name', 'birth_date', 'gender', 'gender_desc',
                  'entered_date', 'personal_phone', 'email', 'status', 'status_desc')


class ProjectSerializer(serializers.ModelSerializer):
    kind = serializers.ChoiceField(choices=Project.KIND_CHOICES)
    kind_desc = serializers.CharField(source='get_kind_display', read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'url', 'company', 'name', 'order', 'kind', 'kind_desc', 'start_year',
                  'is_direct_manage', 'is_returned_area', 'is_unit_set',
                  'local_zipcode', 'local_address1', 'local_address2', 'local_address3',
                  'area_usage', 'build_size', 'num_unit', 'buy_land_extent', 'scheme_land_extent',
                  'donation_land_extent', 'on_floor_area', 'under_floor_area', 'total_floor_area',
                  'build_area', 'floor_area_ratio', 'build_to_land_ratio',
                  'num_legal_parking', 'num_planed_parking')
        extra_kwargs = {'url': {'view_name': 'api:project-detail'}, }


class UnitTypeSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')

    class Meta:
        model = UnitType
        fields = ('id', 'url', 'project', 'name', 'color', 'average_price', 'num_unit')
        extra_kwargs = {'url': {'view_name': 'api:unittype-detail'}, }


class ContractUnitSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')

    class Meta:
        model = ContractUnit
        fields = ('id', 'url', 'project', 'unit_type', 'unit_code', 'contract')
        extra_kwargs = {'url': {'view_name': 'api:contractunit-detail'}}


class UnitNumberSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')

    class Meta:
        model = UnitNumber
        fields = ('id', 'url', 'project', 'unit_type', 'floor_type', 'bldg_no', 'bldg_unit_no',
                  'contract_unit', 'bldg_line', 'floor_no', 'is_hold', 'hold_reason')
        extra_kwargs = {'url': {'view_name': 'api:unitnumber-detail'}}


class ProjectBudgetSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')
    account_d1 = serializers.SlugRelatedField(queryset=ProjectAccountD1.objects.all(), slug_field='name')
    account_d2 = serializers.SlugRelatedField(queryset=ProjectAccountD2.objects.all(), slug_field='name')

    class Meta:
        model = ProjectBudget
        fields = ('id', 'url', 'project', 'account_d1', 'account_d2', 'budget')
        extra_kwargs = {'url': {'view_name': 'api:projectbudget-detail'}}


class SiteSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')

    class Meta:
        model = Site
        fields = ('id', 'url', 'project', 'order', 'district', 'lot_number', 'site_purpose',
                  'official_area', 'returned_area', 'rights_restrictions', 'dup_issue_date')
        extra_kwargs = {'url': {'view_name': 'api:site-detail'}}


class SiteOwnerSerializer(serializers.ModelSerializer):
    # project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')
    own_sort_desc = serializers.CharField(source='get_own_sort_display', read_only=True)

    class Meta:
        model = SiteOwner
        fields = ('id', 'url', 'project', 'owner', 'date_of_birth', 'phone1', 'phone2',
                  'zipcode', 'address1', 'address2', 'address3', 'own_sort', 'own_sort_desc',
                  'sites', 'counsel_record', 'user')
        extra_kwargs = {'url': {'view_name': 'api:siteowner-detail'}}


class SiteOwnshipRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteOwnshipRelationship
        fields = ('id', 'url', 'site', 'site_owner', 'ownership_ratio', 'owned_area', 'acquisition_date')
        extra_kwargs = {'url': {'view_name': 'api:relation-detail'}}


class SiteContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContract
        fields = ('id', 'url', 'project', 'owner', 'contract_date', 'total_price', 'down_pay1', 'down_pay1_is_paid',
                  'down_pay2', 'down_pay2_date', 'down_pay2_is_paid', 'inter_pay1', 'inter_pay1_date',
                  'inter_pay1_is_paid',
                  'inter_pay2', 'inter_pay2_date', 'inter_pay2_is_paid', 'remain_pay', 'remain_pay_date',
                  'remain_pay_is_paid',
                  'ownership_completion', 'acc_bank', 'acc_number', 'acc_owner', 'note')
        extra_kwargs = {'url': {'view_name': 'api:sitecontract-detail'}}


class InlineAccSubD1Serializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSubD1
        fields = ('id', 'url', 'name')
        extra_kwargs = {'url': {'view_name': 'api:acc_d1-detail'}}


class InlineAccSubD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSubD2
        fields = ('id', 'url', 'name')
        extra_kwargs = {'url': {'view_name': 'api:acc_d2-detail'}}


class InlineAccSubD3Serializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSubD3
        fields = ('id', 'url', 'name')
        extra_kwargs = {'url': {'view_name': 'api:acc_d3-detail'}}


class AccountSubD1Serializer(serializers.ModelSerializer):
    acc_d2s = InlineAccSubD2Serializer(many=True, read_only=True)

    class Meta:
        model = AccountSubD1
        fields = ('id', 'url', 'code', 'name', 'description', 'acc_d2s')
        extra_kwargs = {'url': {'view_name': 'api:acc_d1-detail'}}


class AccountSubD2Serializer(serializers.ModelSerializer):
    d1 = InlineAccSubD1Serializer(read_only=True)
    acc_d3s = InlineAccSubD3Serializer(many=True, read_only=True)

    class Meta:
        model = AccountSubD2
        fields = ('id', 'url', 'd1', 'code', 'name', 'description', 'acc_d3s')
        extra_kwargs = {'url': {'view_name': 'api:acc_d2-detail'}}


class AccountSubD3Serializer(serializers.ModelSerializer):
    d2 = InlineAccSubD2Serializer(read_only=True)

    class Meta:
        model = AccountSubD3
        fields = ('id', 'url', 'd2', 'code', 'name', 'is_special', 'description')
        extra_kwargs = {'url': {'view_name': 'api:acc_d3-detail'}}


class InlineProjectAccD1Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAccountD1
        fields = ('id', 'url', 'name')
        extra_kwargs = {'url': {'view_name': 'api:project_acc_d1-detail'}}


class InlineProjectAccD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAccountD2
        fields = ('id', 'url', 'name')
        extra_kwargs = {'url': {'view_name': 'api:project_acc_d2-detail'}}


class ProjectAccountD1Serializer(serializers.ModelSerializer):
    acc_d2s = InlineProjectAccD2Serializer(many=True, read_only=True)
    sort_desc = serializers.CharField(source='get_sort_display', read_only=True)

    class Meta:
        model = ProjectAccountD1
        fields = ('id', 'url', 'sort', 'sort_desc', 'code', 'name', 'description', 'acc_d2s')
        extra_kwargs = {'url': {'view_name': 'api:project_acc_d1-detail'}}


class ProjectAccountD2Serializer(serializers.ModelSerializer):
    d1 = InlineProjectAccD1Serializer(read_only=True)

    class Meta:
        model = ProjectAccountD2
        fields = ('id', 'url', 'd1', 'code', 'sub_title', 'name', 'description')
        extra_kwargs = {'url': {'view_name': 'api:project_acc_d2-detail'}}


class BankCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCode
        fields = ('id', 'code', 'name')


class CompanyBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBankAccount
        fields = ('id', 'url', 'company', 'division', 'bankcode', 'alias_name', 'number',
                  'holder', 'open_date', 'note', 'inactive')
        extra_kwargs = {'url': {'view_name': 'api:com_bank-detail'}}


class CashBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBook
        fields = ('id', 'url', 'company', 'cash_category1', 'cash_category2', 'account',
                  'content', 'trader', 'bank_account', 'income', 'outlay', 'evidence',
                  'note', 'deal_date', 'user', 'created_at', 'updated_at')
        extra_kwargs = {'url': {'view_name': 'api:cashbook-detail'}}


class ProjectBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBankAccount
        fields = ('id', 'url', 'project', 'bankcode', 'alias_name', 'number',
                  'holder', 'open_date', 'note', 'inactive', 'directpay')
        extra_kwargs = {'url': {'view_name': 'api:project_bank-detail'}}


class ProjectCashBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCashBook
        fields = ('id', 'url', 'project', 'cash_category1', 'project_account_d1', 'project_account_d2',
                  'is_record_separate', 'is_contract_payment', 'contract', 'installment_order', 'is_release',
                  'is_refund_contractor', 'content', 'trader', 'bank_account', 'income', 'outlay', 'evidence',
                  'note', 'deal_date', 'user', 'created_at', 'updated_at')
        extra_kwargs = {'url': {'view_name': 'api:project_cashbook-detail'}}


class SalesPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPriceByGT
        fields = ('id', 'url', 'project', 'order_group', 'unit_type', 'unit_floor_type',
                  'price_build', 'price_land', 'price_tax', 'price')
        extra_kwargs = {'url': {'view_name': 'api:price-detail'}}


class InstallmentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentPaymentOrder
        fields = ('id', 'url', 'project', 'pay_sort', 'pay_code', 'pay_time',
                  'pay_name', 'alias_name', 'is_pm_cost', 'pay_due_date', 'extra_due_date')
        extra_kwargs = {'url': {'view_name': 'api:install_order-detail'}}


class DownPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownPayment
        fields = ('id', 'url', 'project', 'order_group', 'unit_type', 'number_payments', 'payment_amount')
        extra_kwargs = {'url': {'view_name': 'api:downpay-detail'}}


class OverDueRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverDueRule
        fields = ('id', 'url', 'project', 'term_start', 'term_end', 'rate_year')
        extra_kwargs = {'url': {'view_name': 'api:over_due_rule-detail'}}


class OrderGroupSerializer(serializers.ModelSerializer):
    sort_desc = serializers.CharField(source='get_sort_display', read_only=True)

    class Meta:
        model = OrderGroup
        fields = ('id', 'url', 'project', 'order_number', 'sort', 'sort_desc', 'order_group_name')
        extra_kwargs = {'url': {'view_name': 'api:order_group-detail'}}


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = (
            'id', 'url', 'project', 'order_group', 'serial_number', 'activation', 'user', 'created_at', 'updated_at')
        extra_kwargs = {'url': {'view_name': 'api:contract-detail'}}


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('id', 'url', 'contract', 'name', 'birth_date', 'gender', 'is_registed',
                  'status', 'reservation_date', 'contract_date', 'note', 'user', 'created_at', 'updated_at')
        extra_kwargs = {'url': {'view_name': 'api:contractor-detail'}}


class ContractorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorAddress
        fields = ('id', 'url', 'contractor', 'id_zipcode', 'id_address1', 'id_address2', 'id_address3',
                  'dm_zipcode', 'dm_address1', 'dm_address2', 'dm_address3', 'user', 'created_at', 'updated_at')
        extra_kwargs = {'url': {'view_name': 'api:cont_address-detail'}}


class ContractorContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorContact
        fields = ('id', 'url', 'contractor', 'cell_phone', 'home_phone', 'other_phone', 'email', 'user', 'created_at',
                  'updated_at')
        extra_kwargs = {'url': {'view_name': 'api:contact-detail'}}


class ContractorReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorRelease
        fields = ('id', 'url', 'project', 'contractor', 'status', 'refund_amount',
                  'refund_account_bank', 'refund_account_number', 'refund_account_depositor',
                  'request_date', 'completion_date', 'note', 'user', 'created_at', 'updated_at')
        extra_kwargs = {'url': {'view_name': 'api:release-detail'}}


class SallesBillIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesBillIssue
        fields = ('id', 'url', 'project', 'now_payment_order', 'host_name', 'host_tel',
                  'agency', 'agency_tel', 'bank_account1', 'bank_number1', 'bank_host1',
                  'bank_account2', 'bank_number2', 'bank_host2', 'zipcode', 'address1', 'address2', 'address3',
                  'title', 'content', 'user', 'updated_at')
        extra_kwargs = {'url': {'view_name': 'api:bill_issue-detail'}}


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'url', 'name', 'manager')
        extra_kwargs = {'url': {'view_name': 'api:group-detail'}}


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'url', 'group', 'name', 'order', 'search_able', 'manager')
        extra_kwargs = {'url': {'view_name': 'api:board-detail'}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'url', 'board', 'name', 'parent', 'order')
        extra_kwargs = {'url': {'view_name': 'api:category-detail'}}


class LawSuitCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawsuitCase
        fields = ('id', 'url', 'project', 'sort', 'level', 'related_case', 'court',
                  'other_agency', 'case_number', 'case_name', 'plaintiff', 'defendant',
                  'related_debtor', 'case_start_date', 'summary', 'user', 'created', 'updated')
        extra_kwargs = {'url': {'view_name': 'api:suitcase-detail'}}


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'url', 'board', 'is_notice', 'project', 'category', 'lawsuit',
                  'title', 'execution_date', 'content', 'is_hide_comment', 'hit', 'like',
                  'dislike', 'blame', 'ip', 'device', 'secret', 'password', 'user', 'soft_delete', 'created', 'updated')
        extra_kwargs = {'url': {'view_name': 'api:post-detail'}}


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'url', 'post', 'image', 'created')
        extra_kwargs = {'url': {'view_name': 'api:image-detail'}}


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'url', 'post', 'link', 'hit')
        extra_kwargs = {'url': {'view_name': 'api:link-detail'}}


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'url', 'post', 'file', 'hit')
        extra_kwargs = {'url': {'view_name': 'api:file-detail'}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'url', 'post', 'content', 'like', 'dislike', 'blame', 'ip', 'device', 'secret', 'password', 'user',
            'soft_delete', 'created', 'updated')
        extra_kwargs = {'url': {'view_name': 'api:comment-detail'}}


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'url', 'board', 'tag', 'post')
        extra_kwargs = {'url': {'view_name': 'api:tag-detail'}}


class WiseSaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WiseSaying
        fields = ('id', 'url', 'saying_ko', 'saying_en', 'spoked_by')
        extra_kwargs = {'url': {'view_name': 'api:wise-say-detail'}}
