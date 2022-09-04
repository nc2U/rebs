from django.db import transaction
from rest_framework import serializers

from rebs.models import (AccountSort, AccountSubD1, AccountSubD2, AccountSubD3,
                         ProjectAccountD1, ProjectAccountD2, CalendarSchedule, WiseSaying)
from cash.models import (BankCode, CompanyBankAccount, ProjectBankAccount,
                         CashBook, ProjectCashBook, SalesPriceByGT,
                         InstallmentPaymentOrder, DownPayment, OverDueRule)
from contract.models import (OrderGroup, Contract, Contractor,
                             ContractorAddress, ContractorContact, ContractorRelease)

from document.models import Group, Board, Category, LawsuitCase, Post, Image, Link, File, Comment, Tag


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
            'content', 'trader', 'bank_account', 'income', 'outlay', 'evidence',
            'evidence_desc', 'note', 'deal_date', 'user', 'created_at', 'updated_at')


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
        fields = ('pk', 'pay_sort', 'pay_time', 'pay_name', '__str__')


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
        fields = ('pk', 'deal_date', 'contract', 'income', 'installment_order',
                  'bank_account', 'trader', 'note')


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
            'pk', 'name', 'birth_date', 'gender', 'is_registed', 'contractoraddress',
            'contractorcontact', 'status', 'reservation_date', 'contract_date', 'note')


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
        payments = instance.payments.filter(project_account_d2__lte=2).order_by('deal_date', 'id')
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
    # contract = ContractInContractorSerializer()
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
                  'bank_account2', 'bank_number2', 'bank_host2', 'zipcode', 'address1',
                  'address2', 'address3', 'title', 'content')


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
        fields = ('pk', 'project', 'sort', 'level', 'related_case', 'court', 'other_agency',
                  'case_number', 'case_name', 'plaintiff', 'defendant', 'related_debtor',
                  'case_start_date', 'summary', 'user', 'created', 'updated')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('pk', 'board', 'is_notice', 'project', 'category', 'lawsuit', 'title',
                  'execution_date', 'content', 'is_hide_comment', 'hit', 'like', 'dislike', 'blame',
                  'ip', 'device', 'secret', 'password', 'user', 'soft_delete', 'created', 'updated')


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
            'pk', 'post', 'content', 'like', 'dislike', 'blame', 'ip', 'device',
            'secret', 'password', 'user', 'soft_delete', 'created', 'updated')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('pk', 'board', 'tag', 'post')


# Etc --------------------------------------------------------------------------
class WiseSaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WiseSaying
        fields = ('pk', 'saying_ko', 'saying_en', 'spoked_by')
