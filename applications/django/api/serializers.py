from rest_framework import serializers

from accounts.models import User, StaffAuth, Profile, Todo
from company.models import Company, Department, Position, Staff
from project.models import (Project, UnitType, UnitFloorType,
                            KeyUnit, BuildingUnit, HouseUnit, ProjectBudget,
                            Site, SiteOwner, SiteOwnshipRelationship, SiteContract)
from rebs.models import (AccountSort, AccountSubD1, AccountSubD2, AccountSubD3,
                         ProjectAccountD1, ProjectAccountD2, WiseSaying)
from cash.models import (BankCode, CompanyBankAccount, ProjectBankAccount,
                         CashBook, ProjectCashBook, SalesPriceByGT,
                         InstallmentPaymentOrder, DownPayment, OverDueRule)
from contract.models import (OrderGroup, Contract, Contractor,
                             ContractorAddress, ContractorContact, ContractorRelease)
from notice.models import SalesBillIssue
from document.models import Group, Board, Category, LawsuitCase, Post, Image, Link, File, Comment, Tag


# Accounts --------------------------------------------------------------------------
class StaffAuthInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAuth
        fields = (
            'pk', 'company', 'is_staff', 'assigned_project', 'allowed_projects',
            'contract', 'payment', 'notice', 'project_cash', 'project_docs', 'project',
            'company_cash', 'company_docs', 'human_resource', 'company_settings', 'auth_manage')


class ProfileInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('pk', 'name', 'birth_date', 'cell_phone', 'image')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='변경할 필요가 없으면 비워 두십시오.',
        style={'input_type': 'password', 'placeholder': '비밀번호'}
    )
    staffauth = StaffAuthInUserSerializer()
    profile = ProfileInUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'pk', 'email', 'username', 'is_active', 'is_superuser',
            'date_joined', 'password', 'staffauth', 'profile')

    def save(self):
        instance = User(email=self.validated_data['email'],
                        username=self.validated_data['username'])
        password = self.validated_data['password']
        instance.set_password(password)
        instance.save()
        self.instance = instance
        return self.instance


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Profile
        fields = ('pk', 'user', 'name', 'birth_date', 'cell_phone', 'image')


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('pk', 'user', 'title', 'completed', 'created_at', 'updated_at', 'soft_deleted')


# Company --------------------------------------------------------------------------
class DepartsInCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('pk', 'upper_depart', 'name', 'task')


class PositionsInCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('pk', 'rank', 'title', 'description')


class CompanySerializer(serializers.ModelSerializer):
    departments = DepartsInCompanySerializer(many=True, read_only=True)
    positions = PositionsInCompanySerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('pk', 'name', 'ceo', 'tax_number', 'org_number',
                  'business_cond', 'business_even', 'es_date', 'op_date', 'zipcode',
                  'address1', 'address2', 'address3', 'departments', 'positions')


class StaffsInDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('pk', 'position', 'name')


class DepartmentSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='name')
    staffs = StaffsInDepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('pk', 'company', 'name', 'task', 'staffs')


class PositionSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='name')

    class Meta:
        model = Position
        fields = ('pk', 'rank', 'title', 'description')


class StaffSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(queryset=Department.objects.all(), slug_field='name')
    gender = serializers.ChoiceField(choices=Staff.GENDER_CHOICES)
    gender_desc = serializers.CharField(source='get_gender_display', read_only=True)
    status = serializers.ChoiceField(choices=Staff.STATUS_CHOICES)
    status_desc = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Staff
        fields = ('pk', 'department', 'position', 'name', 'birth_date', 'gender', 'gender_desc',
                  'entered_date', 'personal_phone', 'email', 'status', 'status_desc')


# Rebs --------------------------------------------------------------------------
class AccountSortSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSort
        fields = ('pk', 'name', 'accounts')


class AccountSubD1Serializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSubD1
        fields = ('pk', 'code', 'name', 'description')


class AccountSubD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSubD2
        fields = ('pk', 'd1', 'code', 'name', 'description')


class AccountSubD3Serializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSubD3
        fields = ('pk', 'd2', 'code', 'name', 'is_special', 'description')


class ProjectAccountD1Serializer(serializers.ModelSerializer):
    sort_desc = serializers.CharField(source='get_sort_display', read_only=True)

    class Meta:
        model = ProjectAccountD1
        fields = ('pk', 'sort_desc', 'code', 'name', 'description')


class ProjectAccountD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAccountD2
        fields = ('pk', 'd1', 'code', 'sub_title', 'name', 'description')


# Project --------------------------------------------------------------------------
class ProjectSerializer(serializers.ModelSerializer):
    kind = serializers.ChoiceField(choices=Project.KIND_CHOICES)
    kind_desc = serializers.CharField(source='get_kind_display', read_only=True)

    class Meta:
        model = Project
        fields = ('pk', 'company', 'name', 'order', 'kind', 'kind_desc', 'start_year',
                  'is_direct_manage', 'is_returned_area', 'is_unit_set',
                  'local_zipcode', 'local_address1', 'local_address2', 'local_address3',
                  'area_usage', 'build_size', 'num_unit', 'buy_land_extent', 'scheme_land_extent',
                  'donation_land_extent', 'on_floor_area', 'under_floor_area', 'total_floor_area',
                  'build_area', 'floor_area_ratio', 'build_to_land_ratio',
                  'num_legal_parking', 'num_planed_parking')


class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = (
            'pk', 'project', 'name', 'color', 'actual_area',
            'supply_area', 'contract_area', 'average_price', 'num_unit')


class SimpleUnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = ('pk', 'name', 'color', 'average_price')


class UnitFloorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitFloorType
        fields = ('pk', 'project', 'start_floor', 'end_floor', 'extra_cond', 'alias_name')


class BuildingUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingUnit
        fields = ('pk', 'project', 'name')


class KeyUnitSerializer(serializers.ModelSerializer):
    houseunit = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = KeyUnit
        fields = ('pk', 'project', 'unit_type', 'unit_code', 'houseunit', 'contract')


class HouseUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseUnit
        fields = ('pk', 'project', 'unit_type', 'floor_type', '__str__', 'building_unit', 'name',
                  'key_unit', 'bldg_line', 'floor_no', 'is_hold', 'hold_reason')


class ContractorInContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('status', 'name')


class ContractInKeyUnitSerializer(serializers.ModelSerializer):
    contractor = ContractorInContractSerializer()

    class Meta:
        model = Contract
        fields = ('pk', 'contractor')


class KeyUnitInHouseUnitSerializer(serializers.ModelSerializer):
    contract = ContractInKeyUnitSerializer()

    class Meta:
        model = KeyUnit
        fields = ('pk', 'contract')


class AllHouseUnitSerializer(serializers.ModelSerializer):
    key_unit = KeyUnitInHouseUnitSerializer()

    class Meta:
        model = HouseUnit
        fields = ('pk', 'unit_type', 'building_unit', 'name',
                  'key_unit', 'bldg_line', 'floor_no', 'is_hold')


class ProAccoD2InBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAccountD2
        fields = ('pk', 'name', 'sub_title')


class ProAccoD1InBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAccountD1
        fields = ('name', 'acc_d2s')


class ProjectBudgetSerializer(serializers.ModelSerializer):
    account_d1 = ProAccoD1InBudgetSerializer()
    account_d2 = ProAccoD2InBudgetSerializer()

    class Meta:
        model = ProjectBudget
        fields = ('pk', 'account_d1', 'account_d2', 'budget')


class ExecAmountToBudget(serializers.ModelSerializer):
    acc_d2 = serializers.IntegerField()
    all_sum = serializers.IntegerField()
    month_sum = serializers.IntegerField()

    class Meta:
        model = ProjectCashBook
        fields = ('acc_d2', 'all_sum', 'month_sum')


class SiteSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')

    class Meta:
        model = Site
        fields = ('pk', 'project', 'order', 'district', 'lot_number', 'site_purpose',
                  'official_area', 'returned_area', 'rights_restrictions', 'dup_issue_date')


class SiteOwnerSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(queryset=Project.objects.all(), slug_field='name')
    own_sort_desc = serializers.CharField(source='get_own_sort_display', read_only=True)

    class Meta:
        model = SiteOwner
        fields = ('pk', 'project', 'owner', 'date_of_birth', 'phone1', 'phone2',
                  'zipcode', 'address1', 'address2', 'address3', 'own_sort', 'own_sort_desc',
                  'sites', 'counsel_record', 'user')


class SiteOwnshipRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteOwnshipRelationship
        fields = ('pk', 'site', 'site_owner', 'ownership_ratio', 'owned_area', 'acquisition_date')


class SiteContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContract
        fields = ('pk', 'project', 'owner', 'contract_date', 'total_price', 'down_pay1', 'down_pay1_is_paid',
                  'down_pay2', 'down_pay2_date', 'down_pay2_is_paid', 'inter_pay1', 'inter_pay1_date',
                  'inter_pay1_is_paid',
                  'inter_pay2', 'inter_pay2_date', 'inter_pay2_is_paid', 'remain_pay', 'remain_pay_date',
                  'remain_pay_is_paid',
                  'ownership_completion', 'acc_bank', 'acc_number', 'acc_owner', 'note')


# Cash --------------------------------------------------------------------------
class BankCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCode
        fields = ('pk', 'code', 'name')


class CompanyBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBankAccount
        fields = ('pk', 'company', 'division', 'bankcode', 'alias_name', 'number',
                  'holder', 'open_date', 'note', 'inactive')


class BalanceByAccountSerializer(serializers.ModelSerializer):
    bank_acc = serializers.CharField()
    date_inc = serializers.IntegerField()
    date_out = serializers.IntegerField()
    inc_sum = serializers.IntegerField()
    out_sum = serializers.IntegerField()

    class Meta:
        model = ProjectCashBook
        fields = ('bank_acc', 'date_inc', 'date_out', 'inc_sum', 'out_sum')


class CashBookSerializer(serializers.ModelSerializer):
    evidence_desc = serializers.CharField(source='get_evidence_display', read_only=True)

    class Meta:
        model = CashBook
        fields = (
            'pk', 'company', 'sort', 'account_d1', 'account_d2', 'account_d3',
            'content', 'trader', 'bank_account', 'income', 'outlay', 'evidence', 'evidence_desc',
            'note', 'deal_date', 'user', 'created_at', 'updated_at')


class ProjectBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBankAccount
        fields = ('pk', 'project', 'bankcode', 'alias_name', 'number', 'holder',
                  'open_date', 'note', 'inactive', 'directpay', 'is_imprest')


class SeparatedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCashBook
        fields = ('pk', 'project', 'project_account_d1', 'project_account_d2', 'separated',
                  'content', 'trader', 'income', 'outlay', 'evidence', 'note',)


class PrBalanceByAccountSerializer(serializers.ModelSerializer):
    bank_acc = serializers.CharField()
    date_inc = serializers.IntegerField()
    date_out = serializers.IntegerField()
    inc_sum = serializers.IntegerField()
    out_sum = serializers.IntegerField()

    class Meta:
        model = ProjectCashBook
        fields = ('bank_acc', 'date_inc', 'date_out', 'inc_sum', 'out_sum')


class ProjectCashBookSerializer(serializers.ModelSerializer):
    evidence_desc = serializers.CharField(source='get_evidence_display', read_only=True)
    sepItems = SeparatedItemsSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectCashBook
        fields = ('pk', 'project', 'sort', 'project_account_d1', 'project_account_d2',
                  'is_separate', 'separated', 'is_imprest', 'sepItems', 'is_contract_payment',
                  'contract', 'installment_order', 'refund_contractor', 'content', 'trader',
                  'bank_account', 'income', 'outlay', 'evidence', 'evidence_desc', 'note', 'deal_date')


class SimpleOrderGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGroup
        fields = ('pk', 'sort', 'order_group_name')


class SimpleContractSerializer(serializers.ModelSerializer):
    order_group = SimpleOrderGroupSerializer()
    unit_type = SimpleUnitTypeSerializer()
    contractor = serializers.SlugRelatedField(queryset=Contractor.objects.all(), slug_field='name')

    class Meta:
        model = Contract
        fields = ('pk', 'order_group', 'unit_type', 'serial_number', 'contractor')


class SimpleInstallmentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentPaymentOrder
        fields = ('pk', 'pay_time', '__str__')


class SimpleProjectBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBankAccount
        fields = ('pk', 'alias_name')


class PaymentSerializer(serializers.ModelSerializer):
    contract = SimpleContractSerializer()
    installment_order = SimpleInstallmentOrderSerializer()
    bank_account = SimpleProjectBankAccountSerializer()

    class Meta:
        model = ProjectCashBook
        fields = ('pk', 'deal_date', 'contract', 'income', 'installment_order', 'bank_account', 'trader', 'note')


class PaymentSummarySerializer(serializers.ModelSerializer):
    unit_type = serializers.IntegerField()
    type_total = serializers.IntegerField()

    class Meta:
        model = Contract
        fields = ('unit_type', 'type_total')


class NumContractByTypeSerializer(serializers.ModelSerializer):
    unit_type = serializers.IntegerField()
    num_cont = serializers.IntegerField()

    class Meta:
        model = UnitType
        fields = ('unit_type', 'num_cont')


class SalesPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPriceByGT
        fields = ('pk', 'project', 'order_group', 'unit_type', 'unit_floor_type',
                  'price_build', 'price_land', 'price_tax', 'price')


class InstallmentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentPaymentOrder
        fields = ('pk', 'project', '__str__', 'pay_sort', 'pay_code', 'pay_time',
                  'pay_name', 'alias_name', 'is_pm_cost', 'pay_due_date', 'extra_due_date')


class DownPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownPayment
        fields = ('pk', 'project', 'order_group', 'unit_type', 'number_payments', 'payment_amount')


class OverDueRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverDueRule
        fields = ('pk', 'project', 'term_start', 'term_end', 'rate_year')


# Contract --------------------------------------------------------------------------
class OrderGroupSerializer(serializers.ModelSerializer):
    sort_desc = serializers.CharField(source='get_sort_display', read_only=True)

    class Meta:
        model = OrderGroup
        fields = ('pk', 'project', 'order_number', 'sort', 'sort_desc', 'order_group_name')


class HouseUnitInKeyUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseUnit
        fields = ('pk', '__str__', 'floor_type')


class KeyUnitInContractListSerializer(serializers.ModelSerializer):
    houseunit = HouseUnitInKeyUnitSerializer()

    class Meta:
        model = KeyUnit
        fields = ('pk', 'unit_code', 'houseunit')


class AddressInContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorAddress
        fields = ('pk', 'id_zipcode', 'id_address1', 'id_address2', 'id_address3',
                  'dm_zipcode', 'dm_address1', 'dm_address2', 'dm_address3')


class ContactInContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorContact
        fields = ('pk', 'cell_phone', 'home_phone', 'other_phone', 'email')


class ContractorInContractListSerializer(serializers.ModelSerializer):
    contractoraddress = AddressInContractorSerializer()
    contractorcontact = ContactInContractorSerializer()

    class Meta:
        model = Contractor
        fields = (
            'pk', 'name', 'birth_date', 'gender', 'is_registed', 'contractoraddress', 'contractorcontact',
            'status', 'reservation_date', 'contract_date', 'note')


class ContractListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('pk', 'project', 'order_group', 'unit_type', 'serial_number', 'activation')


class ProjectCashBookInContractListSerializer(serializers.ModelSerializer):
    installment_order = SimpleInstallmentOrderSerializer()

    class Meta:
        model = ProjectCashBook
        fields = ('pk', 'deal_date', 'income', 'bank_account', 'trader', 'installment_order')


class ContractCustomListSerializer(serializers.ModelSerializer):
    order_group = SimpleOrderGroupSerializer()
    unit_type = SimpleUnitTypeSerializer()
    keyunit = KeyUnitInContractListSerializer()
    contractor = ContractorInContractListSerializer()
    payments = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = (
            'pk', 'project', 'serial_number', 'activation', 'order_group',
            'unit_type', 'keyunit', 'payments', 'contractor')

    def get_payments(self, instance):
        payments = instance.payments.all().order_by('deal_date', 'id')
        return ProjectCashBookInContractListSerializer(payments, many=True, read_only=True).data


class SubsSummarySerializer(serializers.ModelSerializer):
    unit_type = serializers.IntegerField()
    num_cont = serializers.IntegerField()

    class Meta:
        model = Contract
        fields = ('unit_type', 'num_cont')


class ContSummarySerializer(serializers.ModelSerializer):
    order_group = serializers.IntegerField()
    unit_type = serializers.IntegerField()
    num_cont = serializers.IntegerField()

    class Meta:
        model = Contract
        fields = ('order_group', 'unit_type', 'num_cont')


class ContractInContractorSerializer(serializers.ModelSerializer):
    keyunit = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contract
        fields = ('pk', 'serial_number', 'keyunit')


class ContractorSerializer(serializers.ModelSerializer):
    contract = ContractInContractorSerializer()
    contractorrelease = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contractor
        fields = ('pk', 'contract', 'name', '__str__', 'birth_date', 'gender', 'is_registed',
                  'status', 'reservation_date', 'contract_date', 'note', 'contractorrelease')


class ContractorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorAddress
        fields = ('pk', 'contractor', 'id_zipcode', 'id_address1', 'id_address2', 'id_address3',
                  'dm_zipcode', 'dm_address1', 'dm_address2', 'dm_address3')


class ContractorContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorContact
        fields = ('pk', 'contractor', 'cell_phone', 'home_phone', 'other_phone', 'email')


class ContractorReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorRelease
        fields = ('pk', 'project', 'contractor', '__str__', 'status', 'refund_amount',
                  'refund_account_bank', 'refund_account_number', 'refund_account_depositor',
                  'request_date', 'completion_date', 'note')


# Notice --------------------------------------------------------------------------
class SallesBillIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesBillIssue
        fields = ('pk', 'project', 'now_payment_order', 'host_name', 'host_tel',
                  'agency', 'agency_tel', 'bank_account1', 'bank_number1', 'bank_host1',
                  'bank_account2', 'bank_number2', 'bank_host2', 'zipcode', 'address1', 'address2', 'address3',
                  'title', 'content', 'user', 'updated_at')


# Document --------------------------------------------------------------------------
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name', 'manager')


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('pk', 'group', 'name', 'order', 'search_able', 'manager')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'board', 'name', 'parent', 'order')


class LawSuitCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LawsuitCase
        fields = ('pk', 'project', 'sort', 'level', 'related_case', 'court',
                  'other_agency', 'case_number', 'case_name', 'plaintiff', 'defendant',
                  'related_debtor', 'case_start_date', 'summary', 'user', 'created', 'updated')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('pk', 'board', 'is_notice', 'project', 'category', 'lawsuit',
                  'title', 'execution_date', 'content', 'is_hide_comment', 'hit', 'like',
                  'dislike', 'blame', 'ip', 'device', 'secret', 'password', 'user', 'soft_delete', 'created', 'updated')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('pk', 'post', 'image', 'created')


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('pk', 'post', 'link', 'hit')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('pk', 'post', 'file', 'hit')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'pk', 'post', 'content', 'like', 'dislike', 'blame', 'ip', 'device', 'secret', 'password', 'user',
            'soft_delete', 'created', 'updated')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('pk', 'board', 'tag', 'post')


# Etc --------------------------------------------------------------------------
class WiseSaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WiseSaying
        fields = ('pk', 'saying_ko', 'saying_en', 'spoked_by')
