<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { CompanyBank } from '@/store/types/comCash'
import { write_company_cash } from '@/utils/pageAuth'
import { isValidate } from '@/utils/helper'
import { dateFormat, diffDate } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({ bankAcc: { type: Object, required: true } })
const emit = defineEmits([
  'multi-submit',
  'on-delete',
  'close',
  'patch-d3-hide',
  'patch-bank-hide',
])

const delModal = ref()
const alertModal = ref()

const validated = ref(false)

const form = reactive<CompanyBank>({
  pk: undefined,
  division: null,
  bankcode: null,
  alias_name: '',
  number: '',
  holder: '',
  open_date: null,
  note: '',
  is_hide: false,
  inactive: false,
})

watch(form, val => {
  if (val.open_date) form.open_date = dateFormat(val.open_date)
})

const formsCheck = computed(() => {
  if (props.bankAcc) {
    const a = form.pk === props.bankAcc.pk
    const b = form.pk === props.bankAcc.pk
    const c = form.division === props.bankAcc.division
    const d = form.bankcode === props.bankAcc.bankcode
    const e = form.alias_name === props.bankAcc.alias_name
    const f = form.number === props.bankAcc.number
    const g = form.holder === props.bankAcc.holder
    const h = form.open_date === props.bankAcc.open_date
    const i = form.note === props.bankAcc.note
    const j = form.is_hide === props.bankAcc.is_hide
    const k = form.inactive === props.bankAcc.inactive

    return a && b && c && d && e && f && g && h && i && j && k
  } else return false
})

const accountStore = useAccount()
const allowedPeriod = computed(
  () => accountStore.superAuth || diffDate(props.bankAcc.deal_date) <= 30,
)

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    // const payload = !form.is_separate
    //   ? { formData: form, sepData: null }
    //   : { formData: form, sepData: sepItem }

    // if (write_company_cash.value) {
    //   if (props.bankAcc) {
    //     if (allowedPeriod.value) emit('multi-submit', payload)
    //     else
    //       alertModal.value.callModal(
    //         null,
    //         '거래일로부터 30일이 경과한 건은 수정할 수 없습니다. 관리자에게 문의바랍니다.',
    //       )
    //   } else emit('multi-submit', payload)
    // } else alertModal.value.callModal()
    emit('close')
  }
}

const deleteObject = () => {
  emit('on-delete', {
    project: props.bankAcc.project,
    pk: props.bankAcc.pk,
  })
  delModal.value.close()
  emit('close')
}

const patchD3Hide = (payload: { pk: number; is_hide: boolean }) =>
  emit('patch-d3-hide', payload)

const patchBankHide = (payload: any) => emit('patch-bank-hide', payload)

onBeforeMount(() => {
  if (props.bankAcc) {
    form.pk = props.bankAcc.pk
    form.company = props.bankAcc.company
    form.division = props.bankAcc.division
    form.bankcode = props.bankAcc.bankcode
    form.alias_name = props.bankAcc.alias_name
    form.number = props.bankAcc.number
    form.holder = props.bankAcc.holder
    form.open_date = props.bankAcc.open_date
    form.note = props.bankAcc.note
    form.is_hide = props.bankAcc.is_hide
    form.inactive = props.bankAcc.inactive
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
              <CFormLabel class="col-sm-4 col-form-label">부서정보</CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model="form.division"
                  maxlength="10"
                  required
                  placeholder="부서정보"
                >
                  <option value="">---------</option>
                  <option value="1">입금</option>
                  <option value="2">출금</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">거래은행</CFormLabel>
              <CCol sm="8">
                <CFormSelect v-model.number="form.bankcode" required>
                  <option value="">---------</option>
                  <option value="1">입금</option>
                  <option value="2">출금</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계좌별칭
              </CFormLabel>
              <CCol sm="8">
                <CFormInput v-model="form.alias_name" />
              </CCol>
            </CRow>
          </CCol>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계좌번호
              </CFormLabel>
              <CCol sm="8">
                <CFormInput v-model="form.number" />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label"> 예금주</CFormLabel>
              <CCol sm="8">
                <CFormInput v-model="form.holder" />
              </CCol>
            </CRow>
          </CCol>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">개설일자</CFormLabel>
              <CCol sm="8">
                <DatePicker
                  v-model="form.open_date"
                  maxlength="50"
                  placeholder="개설일자"
                  required
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label"></CFormLabel>
              <CCol sm="8" class="pt-1">
                <CFormSwitch
                  id="formSwitchCheckDefault"
                  v-model="form.is_hide"
                  label="목록에서 숨김 여부"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label"></CFormLabel>
              <CCol sm="8" class="pt-1">
                <CFormSwitch
                  id="formSwitchCheckDefault"
                  v-model="form.inactive"
                  label="사용 종료 및 비활성 여부"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
              <CCol sm="10">
                <CFormTextarea v-model="form.note" placeholder="비고" />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol sm="12" class="text-right pt-2">
            <CButton color="success" type="submit">
              거래 계좌 정보 저장하기
            </CButton>
          </CCol>
        </CRow>
      </div>
    </CModalBody>
  </CForm>

  <AlertModal ref="alertModal" />
</template>
