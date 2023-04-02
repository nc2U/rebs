from django.db import transaction
from rest_framework import serializers

from notice.models import SalesBillIssue
from project.models import (Project, ProjectIncBudget, ProjectOutBudget,
                            Site, SiteOwner, SiteOwnshipRelationship, SiteContract)
from rebs.models import ProjectAccountD1, ProjectAccountD3
from cash.models import ProjectCashBook


# Project --------------------------------------------------------------------------
class SallesBillInProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesBillIssue
        fields = ('pk', 'project', 'now_payment_order', 'host_name', 'host_tel',
                  'agency', 'agency_tel', 'bank_account1', 'bank_number1', 'bank_host1',
                  'bank_account2', 'bank_number2', 'bank_host2', 'zipcode', 'address1',
                  'address2', 'address3', 'title', 'content')


class ProjectSerializer(serializers.ModelSerializer):
    kind = serializers.ChoiceField(choices=Project.KIND_CHOICES)
    kind_desc = serializers.CharField(source='get_kind_display', read_only=True)
    salesbillissue = SallesBillInProjectSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('pk', 'company', 'name', 'order', 'kind', 'kind_desc', 'start_year',
                  'is_direct_manage', 'is_returned_area', 'is_unit_set', 'local_zipcode',
                  'local_address1', 'local_address2', 'local_address3', 'area_usage',
                  'build_size', 'num_unit', 'buy_land_extent', 'scheme_land_extent',
                  'donation_land_extent', 'on_floor_area', 'under_floor_area',
                  'total_floor_area', 'build_area', 'floor_area_ratio', 'build_to_land_ratio',
                  'num_legal_parking', 'num_planed_parking', 'salesbillissue')


class ProjectIncBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectIncBudget
        fields = ('pk', 'project', 'account_d1', 'account_d3', 'order_group',
                  'unit_type', 'item_name', 'average_price', 'quantity', 'budget')


class ProjectOutBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectOutBudget
        fields = ('pk', 'project', 'order', 'account_d1', 'account_d3',
                  'account_opt', 'item_name', 'basis_calc', 'budget')


class ProAccoD1InBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAccountD1
        fields = ('name', 'acc_d3s')


class ProAccoD3InBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAccountD3
        fields = ('pk', 'name')


class StatusOutBudgetSerializer(serializers.ModelSerializer):
    account_d1 = ProAccoD1InBudgetSerializer()
    account_d3 = ProAccoD3InBudgetSerializer()

    class Meta:
        model = ProjectOutBudget
        fields = ('pk', 'project', 'order', 'account_d1', 'account_d3',
                  'account_opt', 'item_name', 'basis_calc', 'budget')


class ExecAmountToBudget(serializers.ModelSerializer):
    acc_d3 = serializers.IntegerField()
    all_sum = serializers.IntegerField()
    month_sum = serializers.IntegerField()

    class Meta:
        model = ProjectCashBook
        fields = ('acc_d3', 'all_sum', 'month_sum')


class TotalSiteAreaSerializer(serializers.ModelSerializer):
    project = serializers.IntegerField()
    official = serializers.DecimalField(max_digits=12, decimal_places=7)
    returned = serializers.DecimalField(max_digits=12, decimal_places=7)

    class Meta:
        model = Site
        fields = ('project', 'official', 'returned')


class SiteOwnerInSiteSerializer(serializers.ModelSerializer):
    own_sort_desc = serializers.CharField(source='get_own_sort_display', read_only=True)

    class Meta:
        model = SiteOwner
        fields = ('pk', 'owner', 'own_sort_desc')


class SiteSerializer(serializers.ModelSerializer):
    owners = SiteOwnerInSiteSerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = ('pk', 'project', 'order', 'district', 'lot_number', 'site_purpose',
                  'official_area', 'returned_area', 'rights_restrictions', 'dup_issue_date', 'owners')


class AllSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('pk', '__str__')


class TotalOwnerAreaSerializer(serializers.ModelSerializer):
    project = serializers.IntegerField()
    owned_area = serializers.DecimalField(max_digits=12, decimal_places=7)

    class Meta:
        model = SiteOwner
        fields = ('project', 'owned_area')


class RelationsInSiteOwnerSerializer(serializers.ModelSerializer):
    site = serializers.ReadOnlyField(source='site.pk')
    __str__ = serializers.ReadOnlyField(source='site.__str__')

    class Meta:
        model = SiteOwnshipRelationship
        fields = ('pk', 'site', '__str__', 'ownership_ratio', 'owned_area', 'acquisition_date')


class SiteOwnerSerializer(serializers.ModelSerializer):
    own_sort_desc = serializers.CharField(source='get_own_sort_display', read_only=True)
    sites = RelationsInSiteOwnerSerializer(source='relations', many=True, read_only=True)

    class Meta:
        model = SiteOwner
        fields = ('pk', 'project', 'owner', 'date_of_birth', 'phone1', 'phone2',
                  'zipcode', 'address1', 'address2', 'address3',
                  'own_sort', 'own_sort_desc', 'sites', 'counsel_record')

    @transaction.atomic
    def create(self, validated_data):
        site_owner = SiteOwner.objects.create(**validated_data)
        if 'sites' in self.initial_data:
            sites = self.initial_data.get('sites')
            # for site in sites:
            #     pk = site.get('pk')
            #     ownership_ratio = site.get('ownership_ratio')
            #     owned_area = site.get('owned_area')
            #     acquisition_date = site.get('acquisition_date')
            #     site_instance = Site.objects.get(pk=pk)
            #     SiteOwnshipRelationship(site=site_instance, site_owner=site_owner, ownership_ratio=ownership_ratio,
            #                             owned_area=owned_area, acquisition_date=acquisition_date).save()
            for site in sites:
                site_instance = Site.objects.get(pk=site)
                SiteOwnshipRelationship(site=site_instance, site_owner=site_owner).save()

        site_owner.save()
        return site_owner

    @transaction.atomic
    def update(self, instance, validated_data):
        sites = self.initial_data.get('sites')
        relations = SiteOwnshipRelationship.objects.filter(site_owner=instance)  # .delete()
        stored_sites = []
        for r in relations:
            if r.site.pk in sites:
                stored_sites.append(r.site.pk)
            else:
                r.delete()
        for site in sites:
            if site not in stored_sites:
                new_site = Site.objects.get(pk=site)
                SiteOwnshipRelationship(site=new_site, site_owner=instance).save()

        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class AllOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteOwner
        fields = ('pk', 'owner')


class SiteOwnshipRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteOwnshipRelationship
        fields = ('pk', 'site', 'site_owner', 'ownership_ratio', 'owned_area', 'acquisition_date')


class TotalContractedAreaSerializer(serializers.ModelSerializer):
    project = serializers.IntegerField()
    contracted_area = serializers.DecimalField(max_digits=12, decimal_places=7)

    class Meta:
        model = SiteOwner
        fields = ('project', 'contracted_area')


class SiteContractSerializer(serializers.ModelSerializer):
    owner_desc = SiteOwnerInSiteSerializer(source='owner', read_only=True)

    class Meta:
        model = SiteContract
        fields = ('pk', 'project', 'owner', 'owner_desc', 'contract_date', 'total_price', 'contract_area', 'down_pay1',
                  'down_pay1_is_paid', 'down_pay2', 'down_pay2_date', 'down_pay2_is_paid',
                  'inter_pay1', 'inter_pay1_date', 'inter_pay1_is_paid', 'inter_pay2',
                  'inter_pay2_date', 'inter_pay2_is_paid', 'remain_pay', 'remain_pay_date',
                  'remain_pay_is_paid', 'ownership_completion', 'acc_bank', 'acc_number',
                  'acc_owner', 'note')
