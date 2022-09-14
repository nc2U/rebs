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
        sepData = self.initial_data.get('sepData')
        if sepData:
            sepCashbook_account_d1 = AccountSubD1.objects.get(pk=sepData.get('account_d1'))
            sepCashbook_account_d2 = AccountSubD2.objects.get(pk=sepData.get('account_d2'))
            sepCashbook_account_d3 = AccountSubD3.objects.get(pk=sepData.get('account_d3'))
            sepCashbook_content = sepData.get('content')
            sepCashbook_trader = sepData.get('trader')
            sepCashbook_income = sepData.get('income')
            sepCashbook_outlay = sepData.get('outlay')
            sepCashbook_evidence = sepData.get('evidence')
            sepCashbook_note = sepData.get('note')
            if not sepData.get('pk'):
                sepCashbook = CashBook(company=cashbook.company,
                                       sort=cashbook.sort,
                                       account_d1=sepCashbook_account_d1,
                                       account_d2=sepCashbook_account_d2,
                                       account_d3=sepCashbook_account_d3,
                                       separated=cashbook,
                                       content=sepCashbook_content,
                                       trader=sepCashbook_trader,
                                       bank_account=cashbook.bank_account,
                                       income=sepCashbook_income,
                                       outlay=sepCashbook_outlay,
                                       evidence=sepCashbook_evidence,
                                       note=sepCashbook_note,
                                       deal_date=cashbook.deal_date)
                sepCashbook.save()
            else:
                sepCashbook = CashBook.objects.get(pk=sepData.get('pk'))
                sepCashbook.company = cashbook.company
                sepCashbook.sort = cashbook.sort
                sepCashbook.account_d1 = sepCashbook_account_d1
                sepCashbook.account_d2 = sepCashbook_account_d2
                sepCashbook.account_d3 = sepCashbook_account_d3
                sepCashbook.separated = cashbook
                sepCashbook.content = sepCashbook_content
                sepCashbook.trader = sepCashbook_trader
                sepCashbook.bank_account = cashbook.bank_account
                sepCashbook.income = sepCashbook_income
                sepCashbook.outlay = sepCashbook_outlay
                sepCashbook.evidence = sepCashbook_evidence
                sepCashbook.note = sepCashbook_note
                sepCashbook.deal_date = cashbook.deal_date
                sepCashbook.save()
        return cashbook

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        # 2. sep 정보 확인 후 저장
        sepData = self.initial_data.get('sepData')
        if sepData:
            sepCashbook_account_d1 = AccountSubD1.objects.get(pk=sepData.get('account_d1'))
            sepCashbook_account_d2 = AccountSubD2.objects.get(pk=sepData.get('account_d2'))
            sepCashbook_account_d3 = AccountSubD3.objects.get(pk=sepData.get('account_d3'))
            sepCashbook_content = sepData.get('content')
            sepCashbook_trader = sepData.get('trader')
            sepCashbook_income = sepData.get('income')
            sepCashbook_outlay = sepData.get('outlay')
            sepCashbook_evidence = sepData.get('evidence')
            sepCashbook_note = sepData.get('note')
            if not sepData.get('pk'):
                sepCashbook = CashBook(company=instance.company,
                                       sort=instance.sort,
                                       account_d1=sepCashbook_account_d1,
                                       account_d2=sepCashbook_account_d2,
                                       account_d3=sepCashbook_account_d3,
                                       separated=instance,
                                       content=sepCashbook_content,
                                       trader=sepCashbook_trader,
                                       bank_account=instance.bank_account,
                                       income=sepCashbook_income,
                                       outlay=sepCashbook_outlay,
                                       evidence=sepCashbook_evidence,
                                       note=sepCashbook_note,
                                       deal_date=instance.deal_date)
                sepCashbook.save()
            else:
                sepCashbook = CashBook.objects.get(pk=sepData.get('pk'))
                sepCashbook.company = instance.company
                sepCashbook.sort = instance.sort
                sepCashbook.account_d1 = sepCashbook_account_d1
                sepCashbook.account_d2 = sepCashbook_account_d2
                sepCashbook.account_d3 = sepCashbook_account_d3
                sepCashbook.separated = instance
                sepCashbook.content = sepCashbook_content
                sepCashbook.trader = sepCashbook_trader
                sepCashbook.bank_account = instance.bank_account
                sepCashbook.income = sepCashbook_income
                sepCashbook.outlay = sepCashbook_outlay
                sepCashbook.evidence = sepCashbook_evidence
                sepCashbook.note = sepCashbook_note
                sepCashbook.deal_date = instance.deal_date
                sepCashbook.save()
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
    evidence_desc = serializers.CharField(source='get_evidence_display', read_only=True)
    sepItems = SepItemsInPrCashBookSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectCashBook
        fields = ('pk', 'project', 'sort', 'project_account_d1', 'project_account_d2',
                  'is_separate', 'separated', 'is_imprest', 'sepItems', 'is_contract_payment',
                  'contract', 'installment_order', 'refund_contractor', 'content', 'trader',
                  'bank_account', 'income', 'outlay', 'evidence', 'evidence_desc', 'note', 'deal_date')

    @transaction.atomic
    def create(self, validated_data):
        prCashbook = ProjectCashBook.objects.create(**validated_data)
        prCashbook.save()

        # 2. sep 정보 확인
        sepData = self.initial_data.get('sepData')
        if sepData:
            sepPrCashbook_project_account_d1 = ProjectAccountD1.objects.get(pk=sepData.get('project_account_d1'))
            sepPrCashbook_project_account_d2 = ProjectAccountD2.objects.get(pk=sepData.get('project_account_d2'))
            sepPrCashbook_is_imprest = sepData.get('is_imprest')
            sepPrCashbook_content = sepData.get('content')
            sepPrCashbook_trader = sepData.get('trader')
            sepPrCashbook_income = sepData.get('income')
            sepPrCashbook_outlay = sepData.get('outlay')
            sepPrCashbook_evidence = sepData.get('evidence')
            sepPrCashbook_note = sepData.get('note')
            if not sepData.get('pk'):
                sepPrCashbook = ProjectCashBook(project=prCashbook.project,
                                                sort=prCashbook.sort,
                                                project_account_d1=sepPrCashbook_project_account_d1,
                                                project_account_d2=sepPrCashbook_project_account_d2,
                                                separated=prCashbook,
                                                is_imprest=sepPrCashbook_is_imprest,
                                                content=sepPrCashbook_content,
                                                trader=sepPrCashbook_trader,
                                                bank_account=prCashbook.bank_account,
                                                income=sepPrCashbook_income,
                                                outlay=sepPrCashbook_outlay,
                                                evidence=sepPrCashbook_evidence,
                                                note=sepPrCashbook_note,
                                                deal_date=prCashbook.deal_date)
                sepPrCashbook.save()
            else:
                sepPrCashbook = ProjectCashBook.objects.get(pk=sepData.get('pk'))
                sepPrCashbook.project = prCashbook.project
                sepPrCashbook.sort = prCashbook.sort
                sepPrCashbook.project_account_d1 = sepPrCashbook_project_account_d1
                sepPrCashbook.project_account_d2 = sepPrCashbook_project_account_d2
                sepPrCashbook.separated = prCashbook
                sepPrCashbook.is_imprest = sepPrCashbook_is_imprest
                sepPrCashbook.content = sepPrCashbook_content
                sepPrCashbook.trader = sepPrCashbook_trader
                sepPrCashbook.bank_account = prCashbook.bank_account
                sepPrCashbook.income = sepPrCashbook_income
                sepPrCashbook.outlay = sepPrCashbook_outlay
                sepPrCashbook.evidence = sepPrCashbook_evidence
                sepPrCashbook.note = sepPrCashbook_note
                sepPrCashbook.deal_date = prCashbook.deal_date
                sepPrCashbook.save()
        return prCashbook

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

        # 2. sep 정보 확인
        sepData = self.initial_data.get('sepData')
        if sepData:
            sepPrCashbook_project_account_d1 = ProjectAccountD1.objects.get(pk=sepData.get('project_account_d1'))
            sepPrCashbook_project_account_d2 = ProjectAccountD2.objects.get(pk=sepData.get('project_account_d2'))
            sepPrCashbook_is_imprest = sepData.get('is_imprest')
            sepPrCashbook_content = sepData.get('content')
            sepPrCashbook_trader = sepData.get('trader')
            sepPrCashbook_income = sepData.get('income')
            sepPrCashbook_outlay = sepData.get('outlay')
            sepPrCashbook_evidence = sepData.get('evidence')
            sepPrCashbook_note = sepData.get('note')
            if not sepData.get('pk'):
                sepPrCashbook = ProjectCashBook(project=instance.project,
                                                sort=instance.sort,
                                                project_account_d1=sepPrCashbook_project_account_d1,
                                                project_account_d2=sepPrCashbook_project_account_d2,
                                                separated=instance,
                                                is_imprest=sepPrCashbook_is_imprest,
                                                content=sepPrCashbook_content,
                                                trader=sepPrCashbook_trader,
                                                bank_account=instance.bank_account,
                                                income=sepPrCashbook_income,
                                                outlay=sepPrCashbook_outlay,
                                                evidence=sepPrCashbook_evidence,
                                                note=sepPrCashbook_note,
                                                deal_date=instance.deal_date)
                sepPrCashbook.save()
            else:
                sepPrCashbook = ProjectCashBook.objects.get(pk=sepData.get('pk'))
                sepPrCashbook.project = instance.project
                sepPrCashbook.sort = instance.sort
                sepPrCashbook.project_account_d1 = sepPrCashbook_project_account_d1
                sepPrCashbook.project_account_d2 = sepPrCashbook_project_account_d2
                sepPrCashbook.separated = instance
                sepPrCashbook.is_imprest = sepPrCashbook_is_imprest
                sepPrCashbook.content = sepPrCashbook_content
                sepPrCashbook.trader = sepPrCashbook_trader
                sepPrCashbook.bank_account = instance.bank_account
                sepPrCashbook.income = sepPrCashbook_income
                sepPrCashbook.outlay = sepPrCashbook_outlay
                sepPrCashbook.evidence = sepPrCashbook_evidence
                sepPrCashbook.note = sepPrCashbook_note
                sepPrCashbook.deal_date = instance.deal_date
                sepPrCashbook.save()
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
