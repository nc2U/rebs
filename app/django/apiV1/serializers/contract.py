from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from contract.models import (OrderGroup, Contract, Contractor,
                             ContractorAddress, ContractorContact, ContractorRelease)
from cash.models import ProjectCashBook
from project.models import HouseUnit, KeyUnit

from .project import SimpleUnitTypeSerializer
from .cash import SimpleInstallmentOrderSerializer, SimpleOrderGroupSerializer


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


class KeyUnitInContractSerializer(serializers.ModelSerializer):
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


class ContractorInContractSerializer(serializers.ModelSerializer):
    contractoraddress = AddressInContractorSerializer()
    contractorcontact = ContactInContractorSerializer()

    class Meta:
        model = Contractor
        fields = (
            'pk', 'name', 'birth_date', 'gender', 'is_registed', 'contractoraddress',
            'contractorcontact', 'status', 'reservation_date', 'contract_date', 'note')


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('pk', 'project', 'order_group', 'unit_type', 'serial_number', 'activation')


class ProjectCashBookInContractSerializer(serializers.ModelSerializer):
    installment_order = SimpleInstallmentOrderSerializer()

    class Meta:
        model = ProjectCashBook
        fields = ('pk', 'deal_date', 'income', 'bank_account', 'trader', 'installment_order')


class ContractSetSerializer(serializers.ModelSerializer):
    order_group_desc = SimpleOrderGroupSerializer(source='order_group', read_only=True)
    unit_type_desc = SimpleUnitTypeSerializer(source='unit_type', read_only=True)
    keyunit = KeyUnitInContractSerializer(read_only=True)
    contractor = ContractorInContractSerializer(read_only=True)
    payments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contract
        fields = (
            'pk', 'project', 'order_group', 'unit_type', 'serial_number', 'activation',
            'contractor', 'unit_type_desc', 'order_group_desc', 'keyunit', 'payments')

    def get_payments(self, instance):
        payments = instance.payments.filter(project_account_d2__lte=2).order_by('deal_date', 'id')
        return ProjectCashBookInContractSerializer(payments, many=True, read_only=True).data

    @transaction.atomic
    def create(self, validated_data):
        # 1. 계약정보 테이블 입력
        contract = Contract.objects.create(**validated_data)
        contract.save()

        # 2. 계약 유닛 연결
        keyunit_data = self.initial_data.get('keyunit')
        keyunit = KeyUnit.objects.get(pk=keyunit_data.get('pk'))
        keyunit.contract = contract
        keyunit.save()

        # 3. 동호수 연결
        house_unit_data = keyunit_data.get('houseunit')
        h_unit_id = house_unit_data.get('pk')
        house_unit = HouseUnit.objects.get(pk=h_unit_id)
        house_unit.key_unit = keyunit
        house_unit.save()

        # 4. 계약자 정보 테이블 입력
        contractor_data = self.initial_data.get('contractor')
        contractor = Contractor(contract=contract,
                                name=contractor_data.get('name'),
                                birth_date=contractor_data.get('birth_date'),
                                gender=contractor_data.get('gender'),
                                is_registed=contractor_data.get('is_registed'),
                                status=contractor_data.get('task'),
                                reservation_date=contractor_data.get('reservation_date'),
                                contract_date=contractor_data.get('contract_date'),
                                note=contractor_data.get('note'),
                                user=self.request.user)
        contractor.save()

        # 5. 계약자 주소 테이블 입력
        address_data = contractor_data.get('contractoraddress')
        contractorAddress = ContractorAddress(contractor=contractor,
                                              id_zipcode=address_data.get('id_zipcode'),
                                              id_address1=address_data.get('id_address1'),
                                              id_address2=address_data.get('id_address2'),
                                              id_address3=address_data.get('id_address3'),
                                              dm_zipcode=address_data.get('dm_zipcode'),
                                              dm_address1=address_data.get('dm_address1'),
                                              dm_address2=address_data.get('dm_address2'),
                                              dm_address3=address_data.get('dm_address3'),
                                              user=self.request.user)
        contractorAddress.save()

        # 6. 계약자 연락처 테이블 입력
        contact_data = contractor_data.get('contractorcontact')
        contractorContact = ContractorContact(contractor=contractor,
                                              cell_phone=contact_data.get('cell_phone'),
                                              home_phone=contact_data.get('home_phone'),
                                              other_phone=contact_data.get('other_phone'),
                                              email=contact_data.get('email'),
                                              user=self.request.user)
        contractorContact.save()

        # 7. 계약금 -- 수납 정보 테이블 입력
        payments_data = self.initial_data.get('payments')
        order_group = self.initial_data.get('order_group_desc')
        serial_number = self.initial_data.get('serial_number')
        for payment in payments_data:
            installment_order = payment.get('installment_order')
            downpay = ProjectCashBook(project=self.initial_data.get('project'),
                                      sort=1,
                                      project_account_d1=order_group.get('sort'),
                                      project_account_d2=order_group.get('sort'),
                                      is_contract_payment=True,
                                      contract=contract,
                                      installment_order=installment_order.get('pk'),
                                      content=f'{contractor_data.get("name")}[{serial_number}] 대금납부',
                                      trader=payment.get('trader'),
                                      bank_account=payment.get('bank_account'),
                                      income=payment.get('income'),
                                      deal_date=payment.get('deal_date'),
                                      user=self.request.user)
            downpay.save()

        return contract

    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. 계약정보 테이블 입력
        instance.__dict__.update(**validated_data)
        instance.save()

        # 1-2. 종전 동호수 연결 해제
        try:
            past_UN = instance.keyunit.houseunit
            past_UN.key_unit = None
            past_UN.save()
        except ObjectDoesNotExist:
            pass

        # 2. 계약 유닛 연결
        pastCU = instance.keyunit
        pastCU.contract = None  # 종전 계약의 계약유닛 삭제
        pastCU.save()

        keyunit_data = self.initial_data.get('keyunit')
        keyunit = KeyUnit.objects.get(pk=keyunit_data.get('pk'))
        keyunit.contract = instance
        keyunit.save()

        # 3. 동호수 연결
        house_unit_data = keyunit_data.get('houseunit')
        h_unit_id = house_unit_data.get('pk')
        house_unit = HouseUnit.objects.get(pk=h_unit_id)
        house_unit.key_unit = keyunit
        house_unit.save()

        # 4. 계약자 정보 테이블 입력
        contractor_data = self.initial_data.get('contractor')
        contractor = Contractor.objects.get(contract=instance)
        contractor.name = contractor_data.get('name')
        contractor.birth_date = contractor_data.get('birth_date')
        contractor.gender = contractor_data.get('gender')
        contractor.is_registed = contractor_data.get('is_registed')
        contractor.status = contractor_data.get('task')
        contractor.reservation_date = contractor_data.get('reservation_date')
        contractor.contract_date = contractor_data.get('contract_date')
        contractor.note = contractor_data.get('note')
        contractor.user = self.request.user
        contractor.save()

        # 5. 계약자 주소 테이블 입력
        address_data = contractor_data.get('contractoraddress')
        contractorAddress = ContractorAddress.objects.get(contractor=contractor)
        contractorAddress.id_zipcode = address_data.get('id_zipcode')
        contractorAddress.id_address1 = address_data.get('id_address1')
        contractorAddress.id_address2 = address_data.get('id_address2')
        contractorAddress.id_address3 = address_data.get('id_address3')
        contractorAddress.dm_zipcode = address_data.get('dm_zipcode')
        contractorAddress.dm_address1 = address_data.get('dm_address1')
        contractorAddress.dm_address2 = address_data.get('dm_address2')
        contractorAddress.dm_address3 = address_data.get('dm_address3')
        contractorAddress.user = self.request.user
        contractorAddress.save()

        # 6. 계약자 연락처 테이블 입력
        contact_data = contractor_data.get('contractorcontact')
        contractorContact = ContractorContact.objects.get(contractor=contractor)
        contractorContact.cell_phone = contact_data.get('cell_phone')
        contractorContact.home_phone = contact_data.get('home_phone')
        contractorContact.other_phone = contact_data.get('other_phone')
        contractorContact.email = contact_data.get('email')
        contractorContact.user = self.request.user
        contractorContact.save()

        # 7. 계약금 -- 수납 정보 테이블 입력
        payments_data = self.initial_data.get('payments')
        order_group = self.initial_data.get('order_group_desc')
        serial_number = self.initial_data.get('serial_number')
        for payment in payments_data:
            installment_order = payment.get('installment_order')
            if payment.get('pk'):
                stored_payment = ProjectCashBook.objects.get(pk=payment.get('pk'))
                stored_payment.installment_order = installment_order.get('pk')
                stored_payment.trader = payment.get('trader')
                stored_payment.bank_account = payment.get('bank_account')
                stored_payment.income = payment.get('income')
                stored_payment.deal_date = payment.get('deal_date')
                stored_payment.user = self.request.user
                stored_payment.save()
            else:
                new_downpay = ProjectCashBook(project=self.initial_data.get('project'),
                                              sort=1,
                                              project_account_d1=order_group.get('sort'),
                                              project_account_d2=order_group.get('sort'),
                                              is_contract_payment=True,
                                              contract=instance,
                                              installment_order=installment_order.get('pk'),
                                              content=f'{contractor_data.get("name")}[{serial_number}] 대금납부',
                                              trader=payment.get('trader'),
                                              bank_account=payment.get('bank_account'),
                                              income=payment.get('income'),
                                              deal_date=payment.get('deal_date'),
                                              user=self.request.user)

                new_downpay.save()

        return instance


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
