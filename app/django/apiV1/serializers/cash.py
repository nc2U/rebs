from django.db import transaction
from rest_framework import serializers

from cash.models import (BankCode, CompanyBankAccount, ProjectBankAccount,
                         CashBook, ProjectCashBook, SalesPriceByGT,
                         InstallmentPaymentOrder, DownPayment, OverDueRule)
from contract.models import OrderGroup, Contract, Contractor
from project.models import UnitType
from rebs.models import AccountSort, AccountSubD1, AccountSubD2, AccountSubD3, ProjectAccountD1, ProjectAccountD2

from .project import SimpleUnitTypeSerializer


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


class SepItemsInCashBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBook
        fields = ('pk', 'account_d1', 'account_d2', 'account_d3', 'separated',
                  'content', 'trader', 'income', 'outlay', 'evidence', 'note')


class CashBookSerializer(serializers.ModelSerializer):
    evidence_desc = serializers.CharField(source='get_evidence_display', read_only=True)
    sepItems = SepItemsInCashBookSerializer(many=True, read_only=True)

    class Meta:
        model = CashBook
        fields = (
            'pk', 'company', 'sort', 'account_d1', 'account_d2', 'account_d3',
            'is_separate', 'separated', 'sepItems', 'content', 'trader', 'bank_account',
            'income', 'outlay', 'evidence', 'evidence_desc', 'note', 'deal_date')

    @transaction.atomic
    def create(self, validated_data):
        # 1. 거래정보 입력
        cashbook = CashBook.objects.create(**validated_data)
        cashbook.save()

        # 2. sep 정보 확인
        sep_data = self.initial_data.get('sepData')
        if sep_data:
            sep_cashbook_account_d1 = AccountSubD1.objects.get(pk=sep_data.get('account_d1'))
            sep_cashbook_account_d2 = AccountSubD2.objects.get(pk=sep_data.get('account_d2'))
            sep_cashbook_account_d3 = AccountSubD3.objects.get(pk=sep_data.get('account_d3'))
            sep_cashbook_content = sep_data.get('content')
            sep_cashbook_trader = sep_data.get('trader')
            sep_cashbook_income = sep_data.get('income')
            sep_cashbook_outlay = sep_data.get('outlay')
            sep_cashbook_evidence = sep_data.get('evidence')
            sep_cashbook_note = sep_data.get('note')
            if not sep_data.get('pk'):
                sep_cashbook = CashBook(company=cashbook.company,
                                        sort=cashbook.sort,
                                        account_d1=sep_cashbook_account_d1,
                                        account_d2=sep_cashbook_account_d2,
                                        account_d3=sep_cashbook_account_d3,
                                        separated=cashbook,
                                        content=sep_cashbook_content,
                                        trader=sep_cashbook_trader,
                                        bank_account=cashbook.bank_account,
                                        income=sep_cashbook_income,
                                        outlay=sep_cashbook_outlay,
                                        evidence=sep_cashbook_evidence,
                                        note=sep_cashbook_note,
                                        deal_date=cashbook.deal_date)
                sep_cashbook.save()
            else:
                sep_cashbook = CashBook.objects.get(pk=sep_data.get('pk'))
                sep_cashbook.company = cashbook.company
                sep_cashbook.sort = cashbook.sort
                sep_cashbook.account_d1 = sep_cashbook_account_d1
                sep_cashbook.account_d2 = sep_cashbook_account_d2
                sep_cashbook.account_d3 = sep_cashbook_account_d3
                sep_cashbook.separated = cashbook
                sep_cashbook.content = sep_cashbook_content
                sep_cashbook.trader = sep_cashbook_trader
                sep_cashbook.bank_account = cashbook.bank_account
                sep_cashbook.income = sep_cashbook_income
                sep_cashbook.outlay = sep_cashbook_outlay
                sep_cashbook.evidence = sep_cashbook_evidence
                sep_cashbook.note = sep_cashbook_note
                sep_cashbook.deal_date = cashbook.deal_date
                sep_cashbook.save()
        return cashbook

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.account_d1 = validated_data.get('account_d1', instance.account_d1)
        instance.account_d2 = validated_data.get('account_d2', instance.account_d2)
        instance.account_d3 = validated_data.get('account_d3', instance.account_d3)
        instance.save()

        # 2. sep 정보 확인 후 저장
        sep_data = self.initial_data.get('sepData')
        if sep_data:
            sep_cashbook_account_d1 = AccountSubD1.objects.get(pk=sep_data.get('account_d1'))
            sep_cashbook_account_d2 = AccountSubD2.objects.get(pk=sep_data.get('account_d2'))
            sep_cashbook_account_d3 = AccountSubD3.objects.get(pk=sep_data.get('account_d3'))
            sep_cashbook_content = sep_data.get('content')
            sep_cashbook_trader = sep_data.get('trader')
            sep_cashbook_income = sep_data.get('income')
            sep_cashbook_outlay = sep_data.get('outlay')
            sep_cashbook_evidence = sep_data.get('evidence')
            sep_cashbook_note = sep_data.get('note')
            if not sep_data.get('pk'):
                sep_cashbook = CashBook(company=instance.company,
                                        sort=instance.sort,
                                        account_d1=sep_cashbook_account_d1,
                                        account_d2=sep_cashbook_account_d2,
                                        account_d3=sep_cashbook_account_d3,
                                        separated=instance,
                                        content=sep_cashbook_content,
                                        trader=sep_cashbook_trader,
                                        bank_account=instance.bank_account,
                                        income=sep_cashbook_income,
                                        outlay=sep_cashbook_outlay,
                                        evidence=sep_cashbook_evidence,
                                        note=sep_cashbook_note,
                                        deal_date=instance.deal_date)
                sep_cashbook.save()
            else:
                sep_cashbook = CashBook.objects.get(pk=sep_data.get('pk'))
                sep_cashbook.company = instance.company
                sep_cashbook.sort = instance.sort
                sep_cashbook.account_d1 = sep_cashbook_account_d1
                sep_cashbook.account_d2 = sep_cashbook_account_d2
                sep_cashbook.account_d3 = sep_cashbook_account_d3
                sep_cashbook.separated = instance
                sep_cashbook.content = sep_cashbook_content
                sep_cashbook.trader = sep_cashbook_trader
                sep_cashbook.bank_account = instance.bank_account
                sep_cashbook.income = sep_cashbook_income
                sep_cashbook.outlay = sep_cashbook_outlay
                sep_cashbook.evidence = sep_cashbook_evidence
                sep_cashbook.note = sep_cashbook_note
                sep_cashbook.deal_date = instance.deal_date
                sep_cashbook.save()
        return instance


class ProjectBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBankAccount
        fields = ('pk', 'project', 'bankcode', 'alias_name', 'number', 'holder',
                  'open_date', 'note', 'inactive', 'directpay', 'is_imprest')


class SepItemsInPrCashBookSerializer(serializers.ModelSerializer):
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
    sort_desc = serializers.SlugField(source='sort', read_only=True)
    project_account_d1_desc = serializers.SlugField(source='project_account_d1', read_only=True)
    project_account_d2_desc = serializers.SlugField(source='project_account_d2', read_only=True)
    bank_account_desc = serializers.SlugField(source='bank_account', read_only=True)
    evidence_desc = serializers.CharField(source='get_evidence_display', read_only=True)
    sepItems = SepItemsInPrCashBookSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectCashBook
        fields = ('pk', 'project', 'sort', 'sort_desc', 'project_account_d1', 'project_account_d1_desc',
                  'project_account_d2', 'project_account_d2_desc', 'is_separate', 'separated',
                  'is_imprest', 'sepItems', 'is_contract_payment', 'contract', 'installment_order',
                  'refund_contractor', 'content', 'trader', 'bank_account', 'bank_account_desc',
                  'income', 'outlay', 'evidence', 'evidence_desc', 'note', 'deal_date')

    @transaction.atomic
    def create(self, validated_data):
        pr_cashbook = ProjectCashBook.objects.create(**validated_data)
        pr_cashbook.save()

        # 2. sep 정보 확인
        sep_data = self.initial_data.get('sepData')
        if sep_data:
            sep_pr_cashbook_project_account_d1 = ProjectAccountD1.objects.get(pk=sep_data.get('project_account_d1'))
            sep_pr_cashbook_project_account_d2 = ProjectAccountD2.objects.get(pk=sep_data.get('project_account_d2'))
            sep_pr_cashbook_is_imprest = sep_data.get('is_imprest')
            sep_pr_cashbook_content = sep_data.get('content')
            sep_pr_cashbook_trader = sep_data.get('trader')
            sep_pr_cashbook_income = sep_data.get('income')
            sep_pr_cashbook_outlay = sep_data.get('outlay')
            sep_pr_cashbook_evidence = sep_data.get('evidence')
            sep_pr_cashbook_note = sep_data.get('note')
            if not sep_data.get('pk'):
                sep_pr_cashbook = ProjectCashBook(project=pr_cashbook.project,
                                                  sort=pr_cashbook.sort,
                                                  project_account_d1=sep_pr_cashbook_project_account_d1,
                                                  project_account_d2=sep_pr_cashbook_project_account_d2,
                                                  separated=pr_cashbook,
                                                  is_imprest=sep_pr_cashbook_is_imprest,
                                                  content=sep_pr_cashbook_content,
                                                  trader=sep_pr_cashbook_trader,
                                                  bank_account=pr_cashbook.bank_account,
                                                  income=sep_pr_cashbook_income,
                                                  outlay=sep_pr_cashbook_outlay,
                                                  evidence=sep_pr_cashbook_evidence,
                                                  note=sep_pr_cashbook_note,
                                                  deal_date=pr_cashbook.deal_date)
                sep_pr_cashbook.save()
            else:
                sep_pr_cashbook = ProjectCashBook.objects.get(pk=sep_data.get('pk'))
                sep_pr_cashbook.project = pr_cashbook.project
                sep_pr_cashbook.sort = pr_cashbook.sort
                sep_pr_cashbook.project_account_d1 = sep_pr_cashbook_project_account_d1
                sep_pr_cashbook.project_account_d2 = sep_pr_cashbook_project_account_d2
                sep_pr_cashbook.separated = pr_cashbook
                sep_pr_cashbook.is_imprest = sep_pr_cashbook_is_imprest
                sep_pr_cashbook.content = sep_pr_cashbook_content
                sep_pr_cashbook.trader = sep_pr_cashbook_trader
                sep_pr_cashbook.bank_account = pr_cashbook.bank_account
                sep_pr_cashbook.income = sep_pr_cashbook_income
                sep_pr_cashbook.outlay = sep_pr_cashbook_outlay
                sep_pr_cashbook.evidence = sep_pr_cashbook_evidence
                sep_pr_cashbook.note = sep_pr_cashbook_note
                sep_pr_cashbook.deal_date = pr_cashbook.deal_date
                sep_pr_cashbook.save()
        return pr_cashbook

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.project_account_d1 = validated_data.get('project_account_d1', instance.project_account_d1)
        instance.project_account_d2 = validated_data.get('project_account_d2', instance.project_account_d2)
        instance.save()

        # 2. sep 정보 확인
        sep_data = self.initial_data.get('sepData')
        if sep_data:
            sep_pr_cashbook_project_account_d1 = ProjectAccountD1.objects.get(pk=sep_data.get('project_account_d1'))
            sep_pr_cashbook_project_account_d2 = ProjectAccountD2.objects.get(pk=sep_data.get('project_account_d2'))
            sep_pr_cashbook_is_imprest = sep_data.get('is_imprest')
            sep_pr_cashbook_content = sep_data.get('content')
            sep_pr_cashbook_trader = sep_data.get('trader')
            sep_pr_cashbook_income = sep_data.get('income')
            sep_pr_cashbook_outlay = sep_data.get('outlay')
            sep_pr_cashbook_evidence = sep_data.get('evidence')
            sep_pr_cashbook_note = sep_data.get('note')
            if not sep_data.get('pk'):
                sep_pr_cashbook = ProjectCashBook(project=instance.project,
                                                  sort=instance.sort,
                                                  project_account_d1=sep_pr_cashbook_project_account_d1,
                                                  project_account_d2=sep_pr_cashbook_project_account_d2,
                                                  separated=instance,
                                                  is_imprest=sep_pr_cashbook_is_imprest,
                                                  content=sep_pr_cashbook_content,
                                                  trader=sep_pr_cashbook_trader,
                                                  bank_account=instance.bank_account,
                                                  income=sep_pr_cashbook_income,
                                                  outlay=sep_pr_cashbook_outlay,
                                                  evidence=sep_pr_cashbook_evidence,
                                                  note=sep_pr_cashbook_note,
                                                  deal_date=instance.deal_date)
                sep_pr_cashbook.save()
            else:
                sep_pr_cashbook = ProjectCashBook.objects.get(pk=sep_data.get('pk'))
                sep_pr_cashbook.project = instance.project
                sep_pr_cashbook.sort = instance.sort
                sep_pr_cashbook.project_account_d1 = sep_pr_cashbook_project_account_d1
                sep_pr_cashbook.project_account_d2 = sep_pr_cashbook_project_account_d2
                sep_pr_cashbook.separated = instance
                sep_pr_cashbook.is_imprest = sep_pr_cashbook_is_imprest
                sep_pr_cashbook.content = sep_pr_cashbook_content
                sep_pr_cashbook.trader = sep_pr_cashbook_trader
                sep_pr_cashbook.bank_account = instance.bank_account
                sep_pr_cashbook.income = sep_pr_cashbook_income
                sep_pr_cashbook.outlay = sep_pr_cashbook_outlay
                sep_pr_cashbook.evidence = sep_pr_cashbook_evidence
                sep_pr_cashbook.note = sep_pr_cashbook_note
                sep_pr_cashbook.deal_date = instance.deal_date
                sep_pr_cashbook.save()
        return instance


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
    order_group = serializers.IntegerField()
    unit_type = serializers.IntegerField()
    type_total = serializers.IntegerField()

    class Meta:
        model = ProjectCashBook
        fields = ('order_group', 'unit_type', 'type_total')


class ContNumByTypeSerializer(serializers.ModelSerializer):
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
        fields = ('pk', 'project', '__str__', 'pay_sort', 'pay_code', 'pay_time', 'pay_ratio',
                  'pay_name', 'alias_name', 'is_pm_cost', 'pay_due_date', 'extra_due_date')


class DownPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownPayment
        fields = ('pk', 'project', 'order_group', 'unit_type', 'number_payments', 'payment_amount')


class OverDueRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverDueRule
        fields = ('pk', 'project', 'term_start', 'term_end', 'rate_year')
