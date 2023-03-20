from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from cash.models import ProjectBankAccount, ProjectCashBook
from project.models import Project, ProjectIncBudget
from items.models import UnitType, HouseUnit, KeyUnit
from payment.models import SalesPriceByGT, InstallmentPaymentOrder, DownPayment
from rebs.models import ProjectAccountSort, ProjectAccountD1, ProjectAccountD2
from contract.models import (OrderGroup, Contract, ContractPrice, Contractor,
                             ContractorAddress, ContractorContact, ContractorRelease)

from .items import SimpleUnitTypeSerializer
from .payment import SimpleInstallmentOrderSerializer, SimpleOrderGroupSerializer


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


class ProjectCashBookOrderInContractSerializer(serializers.ModelSerializer):
    installment_order = SimpleInstallmentOrderSerializer()

    class Meta:
        model = ProjectCashBook
        fields = ('installment_order',)


class ProjectCashBookIncsInContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCashBook
        fields = ('income',)


class ContractSetSerializer(serializers.ModelSerializer):
    keyunit = KeyUnitInContractSerializer(read_only=True)
    contractor = ContractorInContractSerializer(read_only=True)
    payments = serializers.SerializerMethodField(read_only=True)
    last_paid_order = serializers.SerializerMethodField(read_only=True)
    total_paid = serializers.SerializerMethodField(read_only=True)
    order_group_desc = SimpleOrderGroupSerializer(source='order_group', read_only=True)
    unit_type_desc = SimpleUnitTypeSerializer(source='unit_type', read_only=True)

    class Meta:
        model = Contract
        fields = (
            'pk', 'project', 'order_group', 'unit_type', 'serial_number', 'activation', 'keyunit',
            'contractor', 'payments', 'last_paid_order', 'total_paid', 'order_group_desc', 'unit_type_desc')

    @staticmethod
    def get_payment_list(instance):
        return instance.payments.filter(project_account_d2__lte=2)

    def get_payments(self, instance):
        payments = self.get_payment_list(instance).order_by('deal_date', 'id')
        return ProjectCashBookInContractSerializer(payments, many=True, read_only=True).data

    def get_last_paid_order(self, instance):
        payments = self.get_payment_list(instance).order_by('-installment_order', '-deal_date').first()
        order_data = ProjectCashBookOrderInContractSerializer(payments, read_only=True).data
        return order_data.get('installment_order') if payments else None

    def get_total_paid(self, instance):
        inc_data = ProjectCashBookIncsInContractSerializer(self.get_payment_list(instance),
                                                           many=True,
                                                           read_only=True).data
        return sum([i.get('income') for i in inc_data])

    @transaction.atomic
    def create(self, validated_data):
        # 1. 계약정보 테이블 입력
        contract = Contract.objects.create(**validated_data)
        contract.save()

        # 2. 계약 유닛 연결
        keyunit_data = self.initial_data.get('keyunit')
        keyunit = KeyUnit.objects.get(pk=keyunit_data)
        keyunit.contract = contract
        keyunit.save()

        # # 분양가격 설정 데이터 불러오기
        # try:
        #     price = ProjectIncBudget.objects.get(project=contract.project,
        #                                          order_group=contract.order_group,
        #                                          unit_type=contract.unit_type).average_price
        # except ProjectIncBudget.DoesNotExist:
        #     price = UnitType.objects.get(pk=contract.unit_type).average_price
        # except UnitType.DoesNotExist:
        #     price = 1000
        #
        # price_build = None
        # price_land = None
        # price_tax = None

        # 3. 동호수 연결
        if self.initial_data.get('houseunit'):
            house_unit_data = self.initial_data.get('houseunit')
            house_unit = HouseUnit.objects.get(pk=house_unit_data)
            house_unit.key_unit = keyunit
            house_unit.save()

        #     # 가격정보 구하기
        #     sales_price = SalesPriceByGT.objects.get(order_group=contract.order_group,
        #                                              unit_type=contract.unit_type,
        #                                              unit_floor_type=house_unit.floor_type)
        #     price = sales_price.price
        #     price_build = sales_price.price_build
        #     price_land = sales_price.price_land
        #     price_tax = sales_price.price_tax
        #
        # # 4. 가격정보 등록
        # # ### 회차 데이터
        # install_order = InstallmentPaymentOrder.objects.filter(project=contract.project)
        #
        # downs = install_order.filter(pay_sort='1')
        # middles = install_order.filter(pay_sort='2')
        # remains = install_order.filter(pay_sort='3')
        #
        # down_num = len(downs.distinct().values_list('pay_code'))
        # middle_num = len(middles.distinct().values_list('pay_code'))
        #
        # down_ratio = downs.first().pay_ratio / 100 if downs.first().pay_ratio else 0.1
        # middle_ratio = middles.first().pay_ratio / 100 if middles.first().pay_ratio else 0.1
        # remain_ratio = remains.first().pay_ratio / 100 if remains.first().pay_ratio else 0.1
        #
        # try:
        #     down_data = DownPayment.objects.get(order_group=contract.order_group,
        #                                         unit_type=contract.unit_type)
        #     down = down_data.payment_amount
        #     remain = price - (price * middle_ratio * middle_num) - (down * down_num)
        # except DownPayment.DoesNotExist:
        #     down = price * down_ratio
        #     remain = down * remain_ratio
        #
        # middle = price * middle_ratio
        #
        # cont_price = ContractPrice(contract=contract,
        #                            price=price,
        #                            price_build=price_build,
        #                            price_land=price_land,
        #                            price_tax=price_tax,
        #                            down_pay=down,
        #                            middle_pay=middle,
        #                            remain_pay=remain)
        # cont_price.save()

        # 5. 계약자 정보 테이블 입력
        contractor_name = self.initial_data.get('name')
        contractor_birth_date = self.initial_data.get('birth_date')
        contractor_gender = self.initial_data.get('gender')
        contractor_is_registed = self.initial_data.get('is_registed')
        contractor_status = self.initial_data.get('status')
        contractor_reservation_date = self.initial_data.get('reservation_date')
        contractor_contract_date = self.initial_data.get('contract_date')
        contractor_note = self.initial_data.get('note')

        contractor = Contractor(contract=contract,
                                name=contractor_name,
                                birth_date=contractor_birth_date,
                                gender=contractor_gender,
                                is_registed=contractor_is_registed,
                                status=contractor_status,
                                reservation_date=contractor_reservation_date,
                                contract_date=contractor_contract_date,
                                note=contractor_note)
        contractor.save()

        # 6. 계약자 주소 테이블 입력
        address_id_zipcode = self.initial_data.get('id_zipcode')
        address_id_address1 = self.initial_data.get('id_address1')
        address_id_address2 = self.initial_data.get('id_address2')
        address_id_address3 = self.initial_data.get('id_address3')
        address_dm_zipcode = self.initial_data.get('dm_zipcode')
        address_dm_address1 = self.initial_data.get('dm_address1')
        address_dm_address2 = self.initial_data.get('dm_address2')
        address_dm_address3 = self.initial_data.get('dm_address3')

        contractor_address = ContractorAddress(contractor=contractor,
                                               id_zipcode=address_id_zipcode,
                                               id_address1=address_id_address1,
                                               id_address2=address_id_address2,
                                               id_address3=address_id_address3,
                                               dm_zipcode=address_dm_zipcode,
                                               dm_address1=address_dm_address1,
                                               dm_address2=address_dm_address2,
                                               dm_address3=address_dm_address3)
        contractor_address.save()

        # 7. 계약자 연락처 테이블 입력
        contact_cell_phone = self.initial_data.get('cell_phone')
        contact_home_phone = self.initial_data.get('home_phone')
        contact_other_phone = self.initial_data.get('other_phone')
        contact_email = self.initial_data.get('email')

        contractor_contact = ContractorContact(contractor=contractor,
                                               cell_phone=contact_cell_phone,
                                               home_phone=contact_home_phone,
                                               other_phone=contact_other_phone,
                                               email=contact_email)
        contractor_contact.save()

        # 8. 계약금 -- 수납 정보 테이블 입력
        if self.initial_data.get('deal_date'):
            project = self.initial_data.get('project')
            payment_project = Project.objects.get(pk=project)
            order_group_sort = self.initial_data.get('order_group_sort')
            payment_account_d1 = ProjectAccountD1.objects.get(pk=order_group_sort)
            payment_account_d2 = ProjectAccountD2.objects.get(pk=order_group_sort)
            ins_order = self.initial_data.get('installment_order')
            payment_installment_order = InstallmentPaymentOrder.objects.get(pk=ins_order)
            payment_serial_number = self.initial_data.get('serial_number')
            payment_trader = self.initial_data.get('trader')
            bank_account = self.initial_data.get('bank_account')
            payment_bank_account = ProjectBankAccount.objects.get(pk=bank_account)
            payment_income = self.initial_data.get('income')
            payment_deal_date = self.initial_data.get('deal_date')

            down_payment = ProjectCashBook(project=payment_project,
                                           sort=ProjectAccountSort.objects.get(pk=1),
                                           project_account_d1=payment_account_d1,
                                           project_account_d2=payment_account_d2,
                                           contract=contract,
                                           installment_order=payment_installment_order,
                                           content=f'{contractor_name}[{payment_serial_number}] 대금납부',
                                           trader=payment_trader,
                                           bank_account=payment_bank_account,
                                           income=payment_income,
                                           deal_date=payment_deal_date)
            down_payment.save()

        return contract

    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. 계약정보 테이블 입력
        instance.__dict__.update(**validated_data)
        instance.order_group = validated_data.get('order_group', instance.order_group)
        instance.unit_type = validated_data.get('unit_type', instance.unit_type)
        instance.save()

        # 1-2. 종전 동호수 연결 해제
        keyunit_data = self.initial_data.get('keyunit')  # keyunit => pk
        keyunit = KeyUnit.objects.get(pk=keyunit_data)

        house_unit_data = self.initial_data.get('houseunit')  # house_unit => pk
        house_unit = HouseUnit.objects.get(pk=house_unit_data) if house_unit_data else None

        if instance.keyunit.pk != keyunit_data:  # 계약유닛이 수정된 경우
            try:  # 종전 동호수가 있는 경우
                old_houseunit = instance.keyunit.houseunit
                if old_houseunit != house_unit_data:  # 동호수가 수정된 경우
                    old_houseunit.key_unit = None  # 해당 동호수를 삭제
                    old_houseunit.save()
            except ObjectDoesNotExist:  # 종전 동호수가 없는 경우
                pass

            # 2. 계약 유닛 연결
            old_keyunit = instance.keyunit
            old_keyunit.contract = None  # 종전 계약의 계약유닛 삭제
            old_keyunit.save()
            keyunit.contract = instance  # 현재 계약건과 변경 유닛을 연결
            keyunit.save()

            # 3. 동호수 연결
            if house_unit_data:
                house_unit.key_unit = keyunit  # 동호수를 계약유닛과 연결
                house_unit.save()
        else:  # 계약유닛이 수정되지 않은 경우
            try:  # 종전 동호수가 있는 경우
                old_houseunit = instance.keyunit.houseunit
                if old_houseunit != house_unit_data:  # 동호수가 수정된 경우
                    old_houseunit.key_unit = None  # 먼저 종전 동호수 삭제
                    old_houseunit.save()

                    # 3. 동호수 연결
                    if house_unit_data:
                        house_unit.key_unit = instance.keyunit  # 변경 동호수를 기존 계약유닛과 연결
                        house_unit.save()
            except ObjectDoesNotExist:  # 종전 동호수가 없는 경우
                # 3. 동호수 연결
                if house_unit_data:
                    house_unit.key_unit = keyunit  # 동호수를 계약유닛과 연결
                    house_unit.save()

        # 4. 계약자 정보 테이블 입력
        contractor_name = self.initial_data.get('name')
        contractor_birth_date = self.initial_data.get('birth_date')
        contractor_gender = self.initial_data.get('gender')
        contractor_is_registed = self.initial_data.get('is_registed')
        contractor_status = self.initial_data.get('status')
        contractor_reservation_date = self.initial_data.get('reservation_date')
        contractor_contract_date = self.initial_data.get('contract_date')
        contractor_note = self.initial_data.get('note')

        contractor = Contractor.objects.get(contract=instance)
        contractor.name = contractor_name
        contractor.birth_date = contractor_birth_date
        contractor.gender = contractor_gender
        contractor.is_registed = contractor_is_registed
        contractor.status = contractor_status
        contractor.reservation_date = contractor_reservation_date
        contractor.contract_date = contractor_contract_date
        contractor.note = contractor_note
        contractor.save()

        # 5. 계약자 주소 테이블 입력
        address_id_zipcode = self.initial_data.get('id_zipcode')
        address_id_address1 = self.initial_data.get('id_address1')
        address_id_address2 = self.initial_data.get('id_address2')
        address_id_address3 = self.initial_data.get('id_address3')
        address_dm_zipcode = self.initial_data.get('dm_zipcode')
        address_dm_address1 = self.initial_data.get('dm_address1')
        address_dm_address2 = self.initial_data.get('dm_address2')
        address_dm_address3 = self.initial_data.get('dm_address3')

        contractor_address = ContractorAddress.objects.get(contractor=contractor)
        contractor_address.id_zipcode = address_id_zipcode
        contractor_address.id_address1 = address_id_address1
        contractor_address.id_address2 = address_id_address2
        contractor_address.id_address3 = address_id_address3
        contractor_address.dm_zipcode = address_dm_zipcode
        contractor_address.dm_address1 = address_dm_address1
        contractor_address.dm_address2 = address_dm_address2
        contractor_address.dm_address3 = address_dm_address3
        contractor_address.save()

        # 6. 계약자 연락처 테이블 입력
        contact_cell_phone = self.initial_data.get('cell_phone')
        contact_home_phone = self.initial_data.get('home_phone')
        contact_other_phone = self.initial_data.get('other_phone')
        contact_email = self.initial_data.get('email')

        contractor_contact = ContractorContact.objects.get(contractor=contractor)
        contractor_contact.cell_phone = contact_cell_phone
        contractor_contact.home_phone = contact_home_phone
        contractor_contact.other_phone = contact_other_phone
        contractor_contact.email = contact_email
        contractor_contact.save()

        # 7. 계약금 -- 수납 정보 테이블 입력
        if self.initial_data.get('deal_date'):
            payment_id = self.initial_data.get('payment')
            project = self.initial_data.get('project')
            payment_project = Project.objects.get(pk=project)
            order_group_sort = self.initial_data.get('order_group_sort')
            payment_account_d1 = ProjectAccountD1.objects.get(pk=order_group_sort)
            payment_account_d2 = ProjectAccountD2.objects.get(pk=order_group_sort)
            ins_order = self.initial_data.get('installment_order')
            payment_installment_order = InstallmentPaymentOrder.objects.get(pk=ins_order)
            payment_serial_number = self.initial_data.get('serial_number')
            payment_trader = self.initial_data.get('trader')
            bank_account = self.initial_data.get('bank_account')
            payment_bank_account = ProjectBankAccount.objects.get(pk=bank_account)
            payment_income = self.initial_data.get('income')
            payment_deal_date = self.initial_data.get('deal_date')

            if payment_id:
                update_payment = ProjectCashBook.objects.get(pk=payment_id)
                update_payment.trader = payment_trader
                update_payment.bank_account = payment_bank_account
                update_payment.income = payment_income
                update_payment.deal_date = payment_deal_date
                update_payment.save()
            else:
                create_payment = ProjectCashBook(project=payment_project,
                                                 sort=ProjectAccountSort.objects.get(pk=1),
                                                 project_account_d1=payment_account_d1,
                                                 project_account_d2=payment_account_d2,
                                                 contract=instance,
                                                 installment_order=payment_installment_order,
                                                 content=f'{contractor_name}[{payment_serial_number}] 대금납부',
                                                 trader=payment_trader,
                                                 bank_account=payment_bank_account,
                                                 income=payment_income,
                                                 deal_date=payment_deal_date)
                create_payment.save()

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

    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. 해지정보 테이블 입력
        instance.__dict__.update(**validated_data)

        contractor = Contractor.objects.get(pk=self.initial_data.get('contractor'))

        try:
            released_done = contractor.contractorrelease.status >= '4'
        except ObjectDoesNotExist:
            released_done = False

        # 미완료인 상태에서 4 -> 처리완료, 5 -> 자격상실 :: 최종 해지 확정 요청이 있을 경우
        if not released_done and self.initial_data.get('status') >= '4':
            # 1. 계약자 정보 현재 상태 변경
            contract = Contract.objects.get(pk=contractor.contract.id)
            keyunit = KeyUnit.objects.get(contract__contractor=contractor)

            completion_date = self.initial_data.get('completion_date')

            # 2. 계약 상태 변경
            contract.serial_number = f"{contract.serial_number}-terminated-{completion_date}"
            contract.activation = False  # 일련번호 활성 해제
            contract.save()

            # 3. 계약유닛 연결 해제
            keyunit.contract = None
            keyunit.save()

            # 4. 동호수 연결 해제
            try:  # 동호수 존재 여부 확인
                unit = keyunit.houseunit
            except ObjectDoesNotExist:
                unit = None
            if unit:
                unit.key_unit = None
                unit.save()

            # 5. 해당 납부분담금 환불처리
            sort = ProjectAccountSort.objects.get(pk=1)  # 입금 종류 선택
            payments = ProjectCashBook.objects.filter(sort=sort, contract=contractor.contract)  # 해당 계약 입금건 전체
            for payment in payments:
                if not released_done:  # 해지 확정 전일 때만 실행
                    refund_d1 = int(contract.order_group.sort)
                    refund_d2 = int(contract.order_group.sort) + 63  # 분양대금 or 분담금 환불 건으로 계정 변경
                    payment.project_account_d1 = ProjectAccountD1.objects.get(pk=refund_d1)
                    payment.project_account_d2 = ProjectAccountD2.objects.get(pk=refund_d2)
                    payment.refund_contractor = contractor  # 환불 계약자 등록
                if completion_date:
                    msg = f'환불 계약 건 - {payment.contract.serial_number} ({completion_date} 환불완료)'
                    append_note = ', ' + msg if payment.note else msg
                    payment.note = payment.note + append_note
                payment.save()

            # 6. 최종 해지상태로 변경
            contractor.is_registed = False  # 인가 등록 취소
            contractor.status = '4'  # 해지 상태로 변경
            contractor.save()

        instance.save()

        return instance
