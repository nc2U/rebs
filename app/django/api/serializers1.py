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


# Etc --------------------------------------------------------------------------
class WiseSaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WiseSaying
        fields = ('pk', 'saying_ko', 'saying_en', 'spoked_by')
