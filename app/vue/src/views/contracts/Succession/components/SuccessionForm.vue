<script lang="ts" setup>
import { reactive, ref, watch, onBeforeMount, computed } from 'vue'
import { write_contract } from '@/utils/pageAuth'
import { isValidate } from '@/utils/helper'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  succession: { type: Object, default: null },
  contractor: { type: Object, default: null },
})

const emit = defineEmits(['on-submit', 'close'])

const alertModal = ref()
const confirmModal = ref()

const validated = ref(false)
const form = reactive({
  pk: null as number | null,
  contractor: '',
  status: '',
  refund_amount: null as number | null,
  refund_account_bank: '',
  refund_account_number: '',
  refund_account_depositor: '',
  request_date: null as string | null,
  completion_date: null as string | null,
  note: '',
})

const formsCheck = computed(() => {
  if (props.succession) {
    const a = form.status === props.succession.status
    const b =
      !form.refund_amount ||
      form.refund_amount === props.succession.refund_amount
    const c = form.refund_account_bank === props.succession.refund_account_bank
    const d =
      form.refund_account_number === props.succession.refund_account_number
    const e =
      form.refund_account_depositor ===
      props.succession.refund_account_depositor
    const f = form.request_date === props.succession.request_date
    const g = form.completion_date === props.succession.completion_date
    const h = form.note === props.succession.note
    return a && b && c && d && e && f && g && h
  } else return false
})

watch(form, val => {
  if (val.request_date) form.request_date = dateFormat(val.request_date)
  if (val.completion_date)
    form.completion_date = dateFormat(val.completion_date)
})

const onSubmit = (event: Event) => {
  if (write_contract.value) {
    if (isValidate(event)) {
      validated.value = true
    } else emit('on-submit', { ...form })
  } else alertModal.value.callModal()
}

const deleteConfirm = () => {
  if (write_contract.value) confirmModal.value.callModal()
  else alertModal.value.callModal()
}

const modalAction = () => alert('this is ready!')

onBeforeMount(() => {
  if (props.succession) {
    form.pk = props.succession.pk
    form.contractor = props.succession.contractor
    form.status = props.succession.status
    form.refund_amount = props.succession.refund_amount
    form.refund_account_bank = props.succession.refund_account_bank
    form.refund_account_number = props.succession.refund_account_number
    form.refund_account_depositor = props.succession.refund_account_depositor
    form.request_date = props.succession.request_date
    form.completion_date = props.succession.completion_date
    form.note = props.succession.note
  } else form.contractor = props.contractor.pk
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
      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">계약자</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.contractor" required readonly>
                <option :value="form.contractor">
                  {{ contractor ? contractor.name : succession.__str__ }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
            <CCol sm="8" class="text-left">
              <CFormSelect v-model="form.status" required>
                <option value="">---------</option>
                <option v-if="succession && succession.status < '4'" value="0">
                  신청 취소
                </option>
                <option v-if="!succession || succession.status < '4'" value="3">
                  해지 신청
                </option>
                <option v-if="succession" value="4">해지 완료</option>
                <option v-if="succession" value="5">자격 상실</option>
              </CFormSelect>
              <small
                v-if="form.status >= '4' && succession.status < '4'"
                class="text-danger"
              >
                해지 완료, 자격 상실 처리된 계약 건은 계약상태로 되돌릴 수
                없으므로 최종 확정된 상태에서만 진행하십시요.
              </small>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              환불(예정)금액
            </CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model.number="form.refund_amount"
                type="number"
                min="0"
                required
                placeholder="환불(예정)금액"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              거래은행(환불계좌)
            </CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.refund_account_bank"
                maxlength="20"
                required
                placeholder="거래은행(환불계좌)"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계좌번호(환불계좌)
            </CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.refund_account_number"
                maxlength="25"
                required
                placeholder="계좌번호(환불계좌)"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              예금주(환불계좌)
            </CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.refund_account_depositor"
                maxlength="20"
                required
                placeholder="예금주(환불계좌)"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label"> 해지신청일</CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="form.request_date"
                required
                placeholder="해지신청일"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              해지(환불)처리일
            </CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="form.completion_date"
                :required="form.status === '4'"
                placeholder="해지종결일"
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
      <CButton type="button" color="light" @click="emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          type="submit"
          :color="succession ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="succession"
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
    <template #header> 계약 해지 정보 - [삭제]</template>
    <template #default>
      삭제 후 복구할 수 없습니다. 해당 건별 수납 정보 삭제를 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
