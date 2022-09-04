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
