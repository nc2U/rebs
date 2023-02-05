<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { usePayment } from '@/store/pinia/payment'
import { useProCash } from '@/store/pinia/proCash'
import { ProjectCashBook } from '@/store/types/proCash'
import { dateFormat, diffDate } from '@/utils/baseMixins'
import { isValidate } from '@/utils/helper'
import { write_payment } from '@/utils/pageAuth'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  contract: { type: Object, default: null },
  payment: { type: Object, default: null },
})

const emit = defineEmits(['on-submit', 'on-delete', 'close'])

const alertModal = ref()
const confirmModal = ref()

const validated = ref(false)
const form = reactive<ProjectCashBook>({
  project: null, // hidden -> index에서 처리
  sort: 1, // hidden -> always
  project_account_d1: null, // hidden
  project_account_d2: null, // hidden
  is_contract_payment: true, // hidden -> always
  contract: null, //  hidden -> 예외 및 신규 매칭 시 코드 확인
  content: '', // hidden
  installment_order: null,
  trader: '',
  bank_account: null,
  income: null,
  note: '',
  deal_date: dateFormat(new Date()),
})

const formsCheck = computed(() => {
  if (props.payment) {
    const io = props.payment.installment_order
      ? props.payment.installment_order.pk
      : null
    const a = form.installment_order && form.installment_order === io
    const b = form.trader && form.trader === props.payment.trader
    const c =
      form.bank_account && form.bank_account === props.payment.bank_account.pk
    const d = form.income && form.income === props.payment.income
    const e = form.note === props.payment.note
    const f =
      form.deal_date.toString() === new Date(props.payment.deal_date).toString()

    return a && b && c && d && e && f
  } else return false
})

const allowedPeriod = computed(() => {
  return props.payment
    ? useAccount().superAuth || diffDate(props.payment.deal_date) <= 90
    : true
})

const paymentStore = usePayment()
const payOrderList = computed(() => paymentStore.payOrderList)

const proCashStore = useProCash()
const proBankAccountList = computed(() => proCashStore.proBankAccountList)

const onSubmit = (event: Event) => {
  if (write_payment.value) {
    if (allowedPeriod.value) {
      if (isValidate(event)) {
        validated.value = true
      } else {
        form.deal_date = dateFormat(form.deal_date)
        const payload = props.payment
          ? { ...{ pk: props.payment.pk }, ...form }
          : form
        emit('on-submit', payload)
      }
    } else
      alertModal.value.callModal(
        null,
        '수납일로부터 90일이 경과한 건은 수정할 수 없습니다. 관리자에게 문의바랍니다.',
      )
  } else alertModal.value.callModal()
}

const deleteConfirm = () => {
  if (write_payment.value) {
    if (allowedPeriod.value) {
      confirmModal.value.callModal()
    } else
      alertModal.value.callModal(
        null,
        '수납일로부터 90일이 경과한 건은 삭제할 수 없습니다. 관리자에게 문의바랍니다.',
      )
  } else alertModal.value.callModal()
}

const modalAction = () => {
  emit('on-delete')
  emit('close')
}

onMounted(() => {
  if (props.payment) {
    const io = props.payment.installment_order
      ? props.payment.installment_order.pk
      : null
    form.installment_order = io
    form.trader = props.payment.trader
    form.bank_account = props.payment.bank_account.pk
    form.income = props.payment.income
    form.note = props.payment.note
    form.deal_date = props.payment.deal_date
  }
  form.project_account_d1 = props.contract.order_group.sort
  form.project_account_d2 = props.contract.order_group.sort
  form.contract = props.contract.pk
  form.content = `${props.contract.contractor.name}[${props.contract.serial_number}] 대금납부`
})
</script>

<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CModalBody class="p-4">
      <CRow class="mb-3">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label"> 수납일자</CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="form.deal_date"
                required
                placeholder="거래일자"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">납부회차</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.installment_order" required>
                <option value="">---------</option>
                <option v-for="po in payOrderList" :key="po.pk" :value="po.pk">
                  {{ po.__str__ }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">수납금액</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model.number="form.income"
                type="number"
                min="0"
                required
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">수납계좌</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.bank_account" required>
                <option value="">---------</option>
                <option
                  v-for="pb in proBankAccountList"
                  :key="pb.pk"
                  :value="pb.pk"
                >
                  {{ pb.alias_name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">입금자명</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.trader"
                v-c-tooltip="{
                  content:
                    '이 란은 반드시 해당 계좌에 기재된 입금자명과 일치하도록 기재하세요.',
                  placement: 'top',
                }"
                maxlength="20"
                required
                placeholder="입금자명"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol>
          <CRow>
            <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
            <CCol sm="10">
              <CFormTextarea v-model="form.note" placeholder="기타 특이사항" />
            </CCol>
          </CRow>
        </CCol>
      </CRow>
    </CModalBody>

    <CModalFooter>
      <CButton type="button" color="light" @click="$emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          type="submit"
          :color="payment ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="payment"
          type="button"
          color="danger"
          @click="deleteConfirm"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header> 건별 수납 정보 - [삭제]</template>
    <template #default>
      삭제 후 복구할 수 없습니다. 해당 건별 수납 정보 삭제를 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
