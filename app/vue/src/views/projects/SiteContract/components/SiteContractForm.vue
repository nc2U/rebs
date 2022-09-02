<script lang="ts" setup>
import { ref, reactive, computed, watch, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { dateFormat } from '@/utils/baseMixins'
import { write_project } from '@/utils/pageAuth'
import { isValidate } from '@/utils/helper'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  contract: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const validated = ref(false)

const pk = ref<number | null>(null)
const form = reactive({
  project: null as number | null,
  owner: null as number | null,
  contract_date: null as string | null,
  total_price: null,
  contract_area: '',
  down_pay1: null,
  down_pay1_is_paid: false,
  down_pay2: null,
  down_pay2_is_paid: false,
  inter_pay1: null,
  inter_pay1_date: null as string | null,
  inter_pay1_is_paid: false,
  inter_pay2: null,
  inter_pay2_date: null as string | null,
  inter_pay2_is_paid: false,
  remain_pay: null,
  remain_pay_date: null as string | null,
  remain_pay_is_paid: false,
  ownership_completion: false,
  acc_bank: '',
  acc_number: '',
  acc_owner: '',
  note: '',
})

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)
const isReturned = computed(() => projectStore.project?.is_returned_area)
const siteStore = useSite()

const formsCheck = computed(() => {
  if (props.contract) {
    const a = form.owner === props.contract.owner
    const b = form.contract_date === props.contract.contract_date
    const c = form.total_price === props.contract.total_price
    const d = form.contract_area === props.contract.contract_area
    const e = form.down_pay1 === props.contract.down_pay1
    const f = form.down_pay1_is_paid === props.contract.down_pay1_is_paid
    const g = form.down_pay2 === props.contract.down_pay2
    const h = form.down_pay2_is_paid === props.contract.down_pay2_is_paid
    const i = form.inter_pay1 === props.contract.inter_pay1
    const j = form.inter_pay1_date === props.contract.inter_pay1_date
    const k = form.inter_pay1_is_paid === props.contract.inter_pay1_is_paid
    const l = form.inter_pay2 === props.contract.inter_pay2
    const m = form.inter_pay2_date === props.contract.inter_pay2_date
    const n = form.inter_pay2_is_paid === props.contract.inter_pay2_is_paid
    const o = form.remain_pay === props.contract.remain_pay
    const p = form.remain_pay_date === props.contract.remain_pay_date
    const q = form.remain_pay_is_paid === props.contract.remain_pay_is_paid
    const r = form.ownership_completion === props.contract.ownership_completion
    const s = form.acc_bank === props.contract.acc_bank
    const t = form.acc_number === props.contract.acc_number
    const u = form.acc_owner === props.contract.acc_owner
    const v = form.note === props.contract.note

    const sky = a && b && c && d && e && f && g && h && i
    const sea = j && k && l && m && n && o && p && q && r
    const air = s && t && u && v

    return sky && sea && air
  } else return false
})

watch(form, val => {
  if (val.contract_date) form.contract_date = dateFormat(val.contract_date)
  if (val.inter_pay1_date)
    form.inter_pay1_date = dateFormat(val.inter_pay1_date)
  if (val.inter_pay2_date)
    form.inter_pay2_date = dateFormat(val.inter_pay2_date)
  if (val.remain_pay_date)
    form.remain_pay_date = dateFormat(val.remain_pay_date)
})

const onSubmit = (event: any) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    const payload = props.contract ? { pk: pk.value, ...form } : { ...form }
    if (write_project) multiSubmit(payload)
    else alertModal.value.callModal()
  }
}

const multiSubmit = (multiPayload: any) => {
  emit('multi-submit', multiPayload)
  emit('close')
}

const deleteObject = () => {
  emit('on-delete', { pk: props.contract.pk, project: props.contract.project })
  delModal.value.visible = false
  emit('close')
}

const deleteConfirm = () => {
  if (write_project) delModal.value.callModal()
  else alertModal.value.callModal()
}

onBeforeMount(() => {
  if (props.contract) {
    pk.value = props.contract.pk
    form.project = props.contract.project
    form.owner = props.contract.owner
    form.contract_date = props.contract.contract_date
    form.total_price = props.contract.total_price
    form.contract_area = props.contract.contract_area
    form.down_pay1 = props.contract.down_pay1
    form.down_pay1_is_paid = props.contract.down_pay1_is_paid
    form.down_pay2 = props.contract.down_pay2
    form.down_pay2_is_paid = props.contract.down_pay2_is_paid
    form.inter_pay1 = props.contract.inter_pay1
    form.inter_pay1_date = props.contract.inter_pay1_date
    form.inter_pay1_is_paid = props.contract.inter_pay1_is_paid
    form.inter_pay2 = props.contract.inter_pay2
    form.inter_pay2_date = props.contract.inter_pay2_date
    form.inter_pay2_is_paid = props.contract.inter_pay2_is_paid
    form.remain_pay = props.contract.remain_pay
    form.remain_pay_date = props.contract.remain_pay_date
    form.remain_pay_is_paid = props.contract.remain_pay_is_paid
    form.ownership_completion = props.contract.ownership_completion
    form.acc_bank = props.contract.acc_bank
    form.acc_number = props.contract.acc_number
    form.acc_owner = props.contract.acc_owner
    form.note = props.contract.note
  }
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
      <div>
        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">소유자</CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model.number="form.owner"
                  required
                  placeholder="소유자"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                총 계약면적
              </CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.contract_area"
                  type="number"
                  min="0"
                  step="0.0000001"
                  placeholder="총 계약면적"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                총 매매가격
              </CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.total_price"
                  min="0"
                  type="number"
                  placeholder="총 매매가격"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계약 체결일
              </CFormLabel>
              <CCol sm="8">
                <DatePicker
                  v-model="form.contract_date"
                  :required="false"
                  maxlength="10"
                  placeholder="계약 체결일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">계약금</CFormLabel>
              <CCol sm="3">
                <CFormInput
                  v-model.number="form.down_pay1"
                  type="number"
                  min="0"
                  placeholder="계약금 - 1차"
                />
              </CCol>
              <CCol sm="2">
                <CFormSwitch
                  id="down_pay1_is_paid"
                  v-model="form.down_pay1_is_paid"
                  label="지급"
                />
              </CCol>

              <CCol sm="3">
                <CFormInput
                  v-model.number="form.down_pay2"
                  type="number"
                  min="0"
                  placeholder="계약금 - 2차"
                />
              </CCol>
              <CCol sm="2">
                <CFormSwitch
                  id="down_pay2_is_paid"
                  v-model="form.down_pay2_is_paid"
                  label="지급"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">
                중도금 (1차)
              </CFormLabel>
              <CCol sm="3">
                <CFormInput
                  v-model.number="form.inter_pay1"
                  type="number"
                  min="0"
                  placeholder="중도금 - 1차"
                />
              </CCol>
              <CCol sm="3">
                <CFormSwitch
                  id="down_pay1_is_paid"
                  v-model="form.inter_pay1_is_paid"
                  label="지급"
                />
              </CCol>

              <CCol sm="3">
                <DatePicker
                  v-model="form.inter_pay1_date"
                  :required="false"
                  maxlength="10"
                  placeholder="중도금1 지급일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                중도금 (1차)
              </CFormLabel>
              <CCol sm="5">
                <CFormInput
                  v-model.number="form.inter_pay1"
                  type="number"
                  min="0"
                  placeholder="중도금 - 1차"
                />
              </CCol>
              <CCol sm="3">
                <CFormSwitch
                  id="down_pay1_is_paid"
                  v-model="form.inter_pay1_is_paid"
                  label="지급"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                중도금1 지급일
              </CFormLabel>
              <CCol sm="8">
                <DatePicker
                  v-model="form.inter_pay1_date"
                  :required="false"
                  maxlength="10"
                  placeholder="중도금1 지급일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                중도금 (1차)
              </CFormLabel>
              <CCol sm="5">
                <CFormInput
                  v-model.number="form.inter_pay1"
                  type="number"
                  min="0"
                  placeholder="중도금 - 1차"
                />
              </CCol>
              <CCol sm="3">
                <CFormSwitch
                  id="down_pay1_is_paid"
                  v-model="form.inter_pay1_is_paid"
                  label="지급"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                중도금1 지급일
              </CFormLabel>
              <CCol sm="8">
                <DatePicker
                  v-model="form.inter_pay1_date"
                  :required="false"
                  maxlength="10"
                  placeholder="중도금1 지급일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">
                입금 은행
              </CFormLabel>
              <CCol sm="3">
                <CFormInput v-model="form.acc_bank" placeholder="입금 은행" />
              </CCol>
              <CCol sm="4">
                <CFormInput v-model="form.acc_number" placeholder="계좌번호" />
              </CCol>
              <CCol sm="3">
                <CFormInput v-model="form.acc_owner" placeholder="예금주" />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">
                특이사항
              </CFormLabel>
              <CCol sm="10">
                <CFormTextarea
                  v-model="form.note"
                  rows="4"
                  placeholder="특이사항"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </div>
    </CModalBody>

    <CModalFooter>
      <CButton type="button" color="light" @click="$emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          type="submit"
          :color="site ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="site"
          type="button"
          color="danger"
          @click="deleteConfirm"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>
  </CForm>

  <ConfirmModal ref="delModal">
    <template #header>
      <CIcon name="cilWarning" />
      사업 부지 정보 삭제
    </template>
    <template #default>
      삭제한 데이터는 복구할 수 없습니다. 해당 사업 부지 정보를
      삭제하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
