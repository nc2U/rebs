<script lang="ts" setup>
import { reactive, ref, watch, nextTick, computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { usePayment } from '@/store/pinia/payment'
import { useProCash } from '@/store/pinia/proCash'
import { PayOrder } from '@/store/types/payment'
import { Payment } from '@/store/types/contract'
import { useRouter } from 'vue-router'
import { isValidate } from '@/utils/helper'
import { numFormat, dateFormat, diffDate } from '@/utils/baseMixins'
import { write_contract } from '@/utils/pageAuth'
import { maska as vMaska } from 'maska'
import { AddressData, callAddress } from '@/components/DaumPostcode/address'
import DaumPostcode from '@/components/DaumPostcode/index.vue'
import ContNavigation from './ContNavigation.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import DatePicker from '@/components/DatePicker/index.vue'

const props = defineProps({
  contract: { type: Object, default: null },
  unitSet: Boolean,
  isUnion: Boolean,
})

const emit = defineEmits(['type-select', 'on-create', 'on-update'])

const address21 = ref()
const address22 = ref()
const delModal = ref()
const alertModal = ref()
const confirmModal = ref()

const sameAddr = ref(false)
const formsCheck = ref(true)
const validated = ref(false)
const form = reactive({
  // contract
  pk: null as number | null,
  order_group: null as number | null,
  order_group_sort: '',
  unit_type: null as number | null,
  serial_number: '',
  activation: true,

  // keyunit & houseunit
  keyunit: null as number | null | string, // 4
  keyunit_code: '',
  houseunit: null as number | null | string, // 5
  // cont_keyunit: '', // 디비 계약 유닛
  // cont_houseunit: '', // 디비 동호 유닛

  // contractor
  name: '', // 7
  birth_date: null as string | Date | null, // 8
  gender: '', // 9
  is_registed: false, // 10
  status: '', // 1
  reservation_date: null as string | Date | null, // 6-1
  contract_date: null as string | Date | null, // 6-2
  note: '', // 28

  // address
  id_zipcode: '', // 20
  id_address1: '', // 21
  id_address2: '', // 22
  id_address3: '', // 23
  dm_zipcode: '', // 24
  dm_address1: '', // 25
  dm_address2: '', // 26
  dm_address3: '', // 27

  // contact
  cell_phone: '', // 11
  home_phone: '', // 12
  other_phone: '', // 13
  email: '', // 14

  // proCash
  payment: null as number | null,
  deal_date: null as string | Date | null, // 15
  income: null as number | null, // 16
  bank_account: null as number | null, // 17
  trader: '', // 18
  installment_order: null as number | null, // 19
})

watch(form, nVal => {
  if (nVal.keyunit_code)
    form.serial_number = `${nVal.keyunit_code}-${form.order_group}`
  if (nVal.order_group)
    form.serial_number = `${form.keyunit_code}-${nVal.order_group}`
  if (nVal.keyunit === '') form.keyunit = null
  if (nVal.houseunit === '') form.houseunit = null

  formsCheck.value = false
})

watch(props, nVal => {
  if (nVal.contract) {
    // contract
    form.pk = props.contract.pk
    form.order_group = props.contract.order_group
    form.order_group_sort = props.contract.order_group_desc.sort
    form.unit_type = props.contract.unit_type
    form.serial_number = props.contract.serial_number
    form.keyunit = props.contract.keyunit.pk
    form.keyunit_code = props.contract.keyunit.unit_code
    form.houseunit = props.contract.keyunit.houseunit
      ? props.contract.keyunit.houseunit.pk
      : ''
    // form.cont_keyunit = props.contract.keyunit.pk
    // form.cont_houseunit = props.contract.keyunit.houseunit
    //   ? props.contract.keyunit.houseunit.pk
    //   : ''

    // contractor
    form.name = props.contract.contractor.name
    form.birth_date = new Date(props.contract.contractor.birth_date)
    form.gender = props.contract.contractor.gender // 9
    form.is_registed = props.contract.contractor.is_registed // 10
    form.status = props.contract.contractor.status
    form.reservation_date =
      props.contract.contractor.reservation_date === null
        ? null
        : new Date(props.contract.contractor.reservation_date)
    form.contract_date =
      props.contract.contractor.contract_date === null
        ? null
        : new Date(props.contract.contractor.contract_date)
    form.note = props.contract.contractor.note

    // address
    if (nVal.contract.contractor.status === '2') {
      // form.addressPk = props.contract.contractor.contractoraddress.pk
      form.id_zipcode = props.contract.contractor.contractoraddress.id_zipcode // 20
      form.id_address1 = props.contract.contractor.contractoraddress.id_address1 // 21
      form.id_address2 = props.contract.contractor.contractoraddress.id_address2 // 22
      form.id_address3 = props.contract.contractor.contractoraddress.id_address3 // 23
      form.dm_zipcode = props.contract.contractor.contractoraddress.dm_zipcode // 24
      form.dm_address1 = props.contract.contractor.contractoraddress.dm_address1
      form.dm_address2 = props.contract.contractor.contractoraddress.dm_address2 // 26
      form.dm_address3 = props.contract.contractor.contractoraddress.dm_address3 // 27
    }
    // contact
    // form.contactPk = props.contract.contractor.contractorcontact.pk //
    form.cell_phone = props.contract.contractor.contractorcontact.cell_phone
    form.home_phone = props.contract.contractor.contractorcontact.home_phone // 11 // 12
    form.other_phone = props.contract.contractor.contractorcontact.other_phone // 13
    form.email = props.contract.contractor.contractorcontact.email // 14
  }
  nextTick(() => (formsCheck.value = true))
})

const contractStore = useContract()
const orderGroupList = computed(() => contractStore.orderGroupList)
const keyUnitList = computed(() => contractStore.keyUnitList)
const houseUnitList = computed(() => contractStore.houseUnitList)

const projectDataStore = useProjectData()
const unitTypeList = computed(() => projectDataStore.unitTypeList)

const proCashStore = useProCash()
const proBankAccountList = computed(() => proCashStore.proBankAccountList)

const paymentStore = usePayment()
const payOrderList = computed(() => paymentStore.payOrderList)

const contLabel = computed(() => (form.status !== '1' ? '계약' : '청약'))
const isContract = computed(() => form.status === '2')
const noStatus = computed(() => form.status === '' && !props.contract)
const downPayOrder = computed(() =>
  payOrderList.value.filter((po: PayOrder) => po.pay_time <= 1),
)

const downPayments = computed(() =>
  props.contract && props.contract.payments.length > 0
    ? props.contract.payments.filter(
        (p: Payment) => p.installment_order.pay_time === 1,
      )
    : [],
)

const allowedPeriod = (paidDate: string) =>
  useAccount().superAuth || diffDate(paidDate) <= 90

const payUpdate = (payment: Payment) => {
  if (allowedPeriod(payment.deal_date)) {
    form.payment = payment.pk
    form.deal_date = new Date(payment.deal_date)
    form.income = payment.income
    form.bank_account = payment.bank_account
    form.trader = payment.trader
    form.installment_order = payment.installment_order.pk
  } else {
    alertModal.value.callModal(
      null,
      '거래일로부터 90일이 경과한 입력 데이터는 수정할 수 없습니다. 관리자에게 문의바랍니다.',
    )
  }
}

const payReset = () => {
  form.payment = null
  form.deal_date = null
  form.income = null
  form.bank_account = null
  form.trader = ''
  form.installment_order = null
}

const getOGSort = (pk: number): string =>
  orderGroupList.value.filter(o => o.pk == pk)[0].sort

const setOGSort = (e: Event) => {
  const pk = Number((e.target as HTMLSelectElement).value)
  form.order_group_sort = getOGSort(pk)
  unitReset(e)
}

const setKeyCode = (e: Event) => {
  form.houseunit = null
  form.keyunit_code = (e.target as HTMLSelectElement).selectedOptions[0].text
}

const unitReset = (event: Event) => {
  if ((event.target as HTMLSelectElement).value === '') formReset()
}

const typeSelect = (event: Event) => {
  emit('type-select', (event.target as HTMLSelectElement).value)
  form.keyunit = null
  form.houseunit = null
}

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    if (write_contract.value) confirmModal.value.callModal()
    else alertModal.value.callModal()
  }
}

const modalAction = () => {
  form.birth_date = form.birth_date ? dateFormat(form.birth_date) : null
  form.reservation_date = form.reservation_date
    ? dateFormat(form.reservation_date)
    : null
  form.contract_date = form.contract_date
    ? dateFormat(form.contract_date)
    : null
  form.deal_date = form.deal_date ? dateFormat(form.deal_date) : null
  if (!props.contract) emit('on-create', form)
  else emit('on-update', form)
  validated.value = false
  confirmModal.value.close()
  // formReset()
}

const deleteContract = () => {
  if (useAccount().superAuth) delModal.value.callModal()
  else alertModal.value.callModal()
}

const addressCallback = (data: AddressData) => {
  const { formNum, zipcode, address1, address3 } = callAddress(data)
  if (formNum === 2) {
    form.id_zipcode = zipcode
    form.id_address1 = address1
    form.id_address2 = ''
    form.id_address3 = address3
    address21.value.$el.nextElementSibling.focus()
  } else if (formNum === 3) {
    form.dm_zipcode = zipcode
    form.dm_address1 = address1
    form.dm_address2 = ''
    form.dm_address3 = address3
    address22.value.$el.nextElementSibling.focus()
  }
}

const toSame = () => {
  if (!sameAddr.value) {
    form.dm_zipcode = form.id_zipcode
    form.dm_address1 = form.id_address1
    form.dm_address2 = form.id_address2
    form.dm_address3 = form.id_address3
  } else {
    form.dm_zipcode = ''
    form.dm_address1 = ''
    form.dm_address2 = ''
    form.dm_address3 = ''
  }
}

const router = useRouter()

const formReset = () => {
  form.pk = null
  form.order_group = null
  form.order_group_sort = ''
  form.unit_type = null
  form.keyunit = null
  form.houseunit = null
  form.keyunit_code = ''

  // form.contractor = null
  form.name = ''
  form.birth_date = null
  form.gender = ''
  form.is_registed = false
  form.status = ''
  form.reservation_date = null
  form.contract_date = null
  form.note = ''

  form.payment = null
  form.deal_date = null
  form.income = null
  form.bank_account = null
  form.trader = ''
  form.installment_order = null

  // form.addressPk = null
  form.id_zipcode = ''
  form.id_address1 = ''
  form.id_address2 = ''
  form.id_address3 = ''
  form.dm_zipcode = ''
  form.dm_address1 = ''
  form.dm_address2 = ''
  form.dm_address3 = ''

  // form.contactPk = null
  form.cell_phone = ''
  form.home_phone = ''
  form.other_phone = ''
  form.email = ''
  contractStore.contract = null
  router.replace({ name: '계약등록 관리' })
  nextTick(() => (formsCheck.value = true))
}

defineExpose({ formReset })
</script>

<template>
  <CCard>
    <CForm
      class="needs-validation"
      novalidate
      :validated="validated"
      @submit.prevent="onSubmit"
    >
      <CCardBody>
        <ContNavigation v-if="contract" :contractor="contract.contractor.pk" />
        <hr v-if="contract" />
        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            구분
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormSelect v-model="form.status" required @change="unitReset">
              <option value="">---------</option>
              <option value="1">청약</option>
              <option value="2">계약</option>
            </CFormSelect>
            <CFormFeedback invalid>구분 항목을 선택하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            차수
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormSelect
              v-model.number="form.order_group"
              required
              :disabled="noStatus"
              @change="setOGSort"
            >
              <option :value="null">---------</option>
              <option
                v-for="order in orderGroupList"
                :key="order.pk"
                :value="order.pk"
              >
                {{ order.order_group_name }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>차수그룹을 선택하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            타입
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormSelect
              v-model="form.unit_type"
              required
              :disabled="form.order_group === null && !contract"
              @change="typeSelect"
            >
              <option :value="null">---------</option>
              <option
                v-for="type in unitTypeList"
                :key="type.pk"
                :value="type.pk"
              >
                {{ type.name }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>유니트 타입을 선택하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            {{ contLabel }}코드
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormSelect
              v-model="form.keyunit"
              required
              :disabled="form.unit_type === null && !contract"
              @change="setKeyCode"
            >
              <option value="">---------</option>
              <option
                v-for="unit in keyUnitList"
                :key="unit.pk"
                :value="unit.pk"
              >
                {{ unit.unit_code }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>
              {{ contLabel }}코드를 선택하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel v-if="unitSet" class="col-md-2 col-lg-1 col-form-label">
            동호수
          </CFormLabel>
          <CCol v-if="unitSet" md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormSelect
              v-model="form.houseunit"
              :disabled="form.keyunit === null && !contract"
            >
              <option value="">---------</option>
              <option
                v-for="house in houseUnitList"
                :key="house.pk"
                :value="house.pk"
              >
                {{ house.__str__ }}
              </option>
            </CFormSelect>
            <CFormFeedback invalid>동호수를 선택하세요.</CFormFeedback>
          </CCol>
        </CRow>

        <hr />

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            {{ contLabel }}일자
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <DatePicker
              v-show="form.status === '1'"
              v-model="form.reservation_date"
              v-maska="'####-##-##'"
              placeholder="청약일자"
              :required="form.status === '1'"
              :disabled="noStatus"
            />
            <DatePicker
              v-show="form.status !== '1'"
              v-model="form.contract_date"
              v-maska="'####-##-##'"
              placeholder="계약일자"
              :required="isContract"
              :disabled="noStatus"
            />
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            {{ contLabel }}자명
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.name"
              type="text"
              maxlength="20"
              :placeholder="`${contLabel}자명을 입력하세요`"
              required
              :disabled="noStatus"
            />
            <CFormFeedback invalid>
              {{ contLabel }}자명을 입력하세요.
            </CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            생년월일
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <DatePicker
              v-model="form.birth_date"
              v-maska="'####-##-##'"
              maxlength="10"
              placeholder="생년월일"
              :required="isContract"
              :disabled="noStatus"
            />
            <CFormFeedback invalid>생년월일 입력하세요.</CFormFeedback>
          </CCol>

          <CCol v-show="isContract" xs="5" lg="1" class="pt-2 p-0 text-center">
            <div class="form-check form-check-inline">
              <input
                id="male"
                v-model="form.gender"
                class="form-check-input"
                type="radio"
                value="M"
                name="gender"
                :required="isContract"
                :disabled="!isContract"
              />
              <label class="form-check-label" for="male">남</label>
            </div>
            <div class="form-check form-check-inline">
              <input
                id="female"
                v-model="form.gender"
                class="form-check-input"
                type="radio"
                value="F"
                name="gender"
                :disabled="!isContract"
              />
              <label class="form-check-label" for="female">여</label>
            </div>
            <CFormFeedback invalid>성별을 선택하세요.</CFormFeedback>
          </CCol>

          <CCol v-show="isContract && isUnion" xs="6" lg="2" class="pt-2 p-0">
            <CFormSwitch
              id="is_registed"
              v-model="form.is_registed"
              label="인가등록여부"
              :disabled="!isContract"
            />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            휴대전화
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <input
              v-model="form.cell_phone"
              v-maska="['###-###-####', '###-####-####']"
              type="text"
              class="form-control"
              maxlength="13"
              placeholder="휴대전화번호를 선택하세요"
              required
              :disabled="noStatus"
            />
            <CFormFeedback invalid>휴대전화번호를 입력하세요.</CFormFeedback>
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            집전화
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <input
              v-model="form.home_phone"
              v-maska="['###-###-####', '###-####-####']"
              type="text"
              class="form-control"
              maxlength="13"
              placeholder="집전화번호를 선택하세요"
              :disabled="noStatus"
            />
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            기타 연락처
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <input
              v-model="form.other_phone"
              v-maska="['###-###-####', '###-####-####']"
              type="text"
              class="form-control"
              maxlength="13"
              placeholder="기타 연락처를 입력하세요."
              :disabled="noStatus"
            />
          </CCol>

          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            이메일
          </CFormLabel>
          <CCol md="10" lg="2" class="mb-md-3 mb-lg-0">
            <CFormInput
              v-model="form.email"
              type="email"
              maxlength="30"
              placeholder="이메일 주소를 입력하세요."
              :disabled="noStatus"
            />
          </CCol>
        </CRow>

        <CRow class="mb-0">
          <CAlert
            :color="$store.state.theme === 'dark' ? 'default' : 'secondary'"
            class="pb-0"
          >
            <CRow v-if="downPayments.length" class="mb-3">
              <CCol>
                <CRow
                  v-for="(payment, i) in downPayments"
                  :key="payment.pk"
                  class="text-center mb-1"
                  :class="
                    form.payment === payment.pk
                      ? 'text-success text-decoration-underline'
                      : ''
                  "
                >
                  <CCol>
                    계약금
                    <router-link
                      v-c-tooltip="'전체 건별수납 관리'"
                      :to="{
                        name: '건별수납 관리',
                        query: { contract: contract.pk },
                      }"
                    >
                      납부내역
                    </router-link>
                    [{{ i + 1 }}]
                  </CCol>
                  <CCol class="text-right">{{ payment.deal_date }}</CCol>
                  <CCol class="text-right">
                    <router-link
                      v-c-tooltip="'전체 건별수납 관리'"
                      :to="{
                        name: '건별수납 관리',
                        query: { contract: contract.pk },
                      }"
                    >
                      {{ numFormat(payment.income) }}
                    </router-link>
                  </CCol>
                  <CCol>
                    {{
                      proBankAccountList
                        .filter(b => b.pk === payment.bank_account)
                        .map(b => b.alias_name)[0]
                    }}
                  </CCol>
                  <CCol>{{ payment.trader }}</CCol>
                  <CCol>
                    {{ payment.installment_order.__str__ }}
                  </CCol>
                  <CCol>
                    <CButton
                      type="button"
                      color="success"
                      size="sm"
                      @click="payUpdate(payment)"
                    >
                      수정
                    </CButton>
                  </CCol>
                </CRow>
              </CCol>
            </CRow>
            <CRow>
              <CFormLabel class="col-md-2 col-lg-1 col-form-label">
                {{ contLabel }}금 {{ !form.payment ? '등록' : '수정' }}
              </CFormLabel>
              <CCol md="10" lg="2" class="mb-3 mb-lg-0">
                <DatePicker
                  v-model="form.deal_date"
                  v-maska="'####-##-##'"
                  placeholder="입금일자"
                  maxlength="10"
                  :required="!contract"
                  :disabled="noStatus"
                />
              </CCol>

              <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

              <CCol md="5" lg="2" class="mb-3 mb-lg-0">
                <CFormInput
                  v-model="form.income"
                  type="number"
                  min="0"
                  placeholder="입금액"
                  :required="!contract || form.deal_date"
                  :disabled="noStatus"
                />
                <CFormFeedback invalid>입금액을 입력하세요.</CFormFeedback>
              </CCol>

              <CCol md="5" lg="2" class="mb-3 mb-lg-0">
                <CFormSelect
                  v-model="form.bank_account"
                  :required="!contract || form.deal_date"
                  :disabled="noStatus"
                >
                  <option value="">납부계좌 선택</option>
                  <option
                    v-for="pb in proBankAccountList"
                    :key="pb.pk"
                    :value="pb.pk"
                  >
                    {{ pb.alias_name }}
                  </option>
                </CFormSelect>
                <CFormFeedback invalid>납부계좌를 선택하세요.</CFormFeedback>
              </CCol>

              <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

              <CCol md="5" lg="2" class="mb-3 mb-lg-0">
                <CFormInput
                  v-model="form.trader"
                  maxlength="20"
                  placeholder="입금자명을 입력하세요"
                  :required="!contract || form.deal_date"
                  :disabled="noStatus"
                />
                <CFormFeedback invalid>입금자명을 입력하세요.</CFormFeedback>
              </CCol>
              <CCol md="5" lg="2" class="mb-md-3 mb-lg-0">
                <CFormSelect
                  v-model="form.installment_order"
                  :required="!contract || form.deal_date"
                  :disabled="noStatus"
                >
                  <option value="">납부회차 선택</option>
                  <option
                    v-for="po in downPayOrder"
                    :key="po.pk"
                    :value="po.pk"
                  >
                    {{ po.__str__ }}
                  </option>
                </CFormSelect>
                <CFormFeedback invalid>납부회차를 선택하세요.</CFormFeedback>
              </CCol>

              <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

              <CCol v-if="form.payment" xs="3" md="2" lg="1" class="pt-2 mb-3">
                <router-link to="" @click="payReset">Reset</router-link>
              </CCol>
            </CRow>
          </CAlert>
        </CRow>

        <CRow v-show="isContract" class="mb-0">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            주민등록 주소
          </CFormLabel>
          <CCol md="3" lg="2" class="mb-3 mb-lg-0">
            <CInputGroup>
              <CInputGroupText @click="$refs.postCode.initiate(2)">
                우편번호
              </CInputGroupText>
              <CFormInput
                v-model="form.id_zipcode"
                v-maska="'#####'"
                type="text"
                maxlength="5"
                placeholder="우편번호"
                :required="isContract"
                :disabled="!isContract"
                @focus="$refs.postCode.initiate(2)"
              />
              <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>
            </CInputGroup>
          </CCol>

          <CCol md="7" lg="4" class="mb-3 mb-lg-0">
            <CFormInput
              v-model="form.id_address1"
              type="text"
              maxlength="35"
              placeholder="주민등록 주소를 입력하세요"
              :required="isContract"
              :disabled="!isContract"
              @focus="$refs.postCode.initiate(2)"
            />
            <CFormFeedback invalid>주민등록 주소를 입력하세요.</CFormFeedback>
          </CCol>

          <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

          <CCol md="6" lg="2" class="mb-3 mb-lg-0">
            <CFormInput
              ref="address21"
              v-model="form.id_address2"
              type="text"
              maxlength="20"
              placeholder="상세주소를 입력하세요"
              :disabled="!isContract"
            />
            <CFormFeedback invalid>상세주소를 입력하세요.</CFormFeedback>
          </CCol>
          <CCol md="4" lg="2">
            <CFormInput
              v-model="form.id_address3"
              type="text"
              maxlength="20"
              placeholder="참고항목을 입력하세요"
              :disabled="!isContract"
            />
          </CCol>
        </CRow>

        <CRow v-show="isContract" class="mb-0">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            우편수령 주소
          </CFormLabel>
          <CCol md="3" lg="2" class="mb-3 mb-lg-0">
            <CInputGroup>
              <CInputGroupText @click="$refs.postCode.initiate(3)">
                우편번호
              </CInputGroupText>
              <CFormInput
                v-model="form.dm_zipcode"
                v-maska="'#####'"
                type="text"
                maxlength="5"
                placeholder="우편번호"
                :required="isContract"
                :disabled="!isContract"
                @focus="$refs.postCode.initiate(3)"
              />
              <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>
            </CInputGroup>
          </CCol>

          <CCol md="7" lg="4" class="mb-3 mb-lg-0">
            <CFormInput
              v-model="form.dm_address1"
              type="text"
              maxlength="50"
              placeholder="우편물 수령 주소를 입력하세요"
              :required="isContract"
              :disabled="!isContract"
              @focus="$refs.postCode.initiate(3)"
            />
            <CFormFeedback invalid>
              우편물 수령 주소를 입력하세요.
            </CFormFeedback>
          </CCol>

          <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

          <CCol md="6" lg="2" class="mb-3 mb-lg-0">
            <CFormInput
              ref="address22"
              v-model="form.dm_address2"
              type="text"
              maxlength="30"
              placeholder="상세주소를 입력하세요"
              :disabled="!isContract"
            />
            <CFormFeedback invalid>상세주소를 입력하세요.</CFormFeedback>
          </CCol>
          <CCol md="4" lg="2">
            <CFormInput
              v-model="form.dm_address3"
              type="text"
              maxlength="30"
              placeholder="참고항목을 입력하세요"
              :disabled="!isContract"
            />
          </CCol>

          <CCol md="2" class="d-none d-md-block d-lg-none"></CCol>

          <CCol md="10" lg="1" class="pt-2 mb-3">
            <CFormCheck
              id="to-same"
              v-model="sameAddr"
              label="상동"
              :disabled="!isContract || !form.id_zipcode"
              @click="toSame"
            />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel class="col-md-2 col-lg-1 col-form-label">
            비고
          </CFormLabel>
          <CCol md="10" lg="11" class="mb-md-3 mb-lg-0">
            <CFormTextarea
              v-model.number="form.note"
              placeholder="기타 특이사항"
              :disabled="noStatus"
            />
          </CCol>
        </CRow>
      </CCardBody>

      <CCardFooter class="text-right">
        <CButton type="button" color="light" @click="formReset"> 취소</CButton>
        <CButton
          v-if="contract"
          type="button"
          color="danger"
          @click="deleteContract"
        >
          삭제
        </CButton>
        <CButton
          type="submit"
          :color="contract ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          <CIcon name="cil-check-circle" />
          저장
        </CButton>
      </CCardFooter>
    </CForm>
  </CCard>

  <DaumPostcode ref="postCode" @addressCallback="addressCallback" />

  <ConfirmModal ref="delModal">
    <template #header>프로젝트정보 삭제</template>
    <template #default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template #footer>
      <CButton color="danger" disabled="">삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="confirmModal">
    <template #header> {{ contLabel }} 정보 등록 </template>
    <template #default>
      {{ contLabel }} 정보 {{ contract ? '수정등록' : '신규등록' }}을
      진행하시겠습니까?
    </template>
    <template #footer>
      <CButton
        :color="contract ? 'success' : 'primary'"
        :disabled="formsCheck"
        @click="modalAction"
      >
        저장
      </CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
