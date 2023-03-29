<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount, watch } from 'vue'
import { useCompany } from '@/store/pinia/company'
import { useComCash } from '@/store/pinia/comCash'
import { CompanyBank } from '@/store/types/comCash'
import { write_company_cash } from '@/utils/pageAuth'
import { isValidate } from '@/utils/helper'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({ bankAcc: { type: Object, required: true } })
const emit = defineEmits(['on-bank-update'])

const confirmModal = ref()
const alertModal = ref()

const validated = ref(false)

const form = reactive<CompanyBank>({
  pk: undefined,
  depart: null,
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
    const c = form.depart === props.bankAcc.depart
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

const comStore = useCompany()
const getSlugDeparts = computed(() => comStore.getSlugDeparts)

const comCashStore = useComCash()
const bankCodeList = computed(() => comCashStore.bankCodeList)

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    if (write_company_cash.value) {
      confirmModal.value.callModal()
    } else alertModal.value.callModal()
  }
}

const onBankUpdate = () => {
  emit('on-bank-update', { ...form })
  confirmModal.value.close()
}

onBeforeMount(() => {
  if (props.bankAcc) {
    form.pk = props.bankAcc.pk
    form.company = props.bankAcc.company
    form.depart = props.bankAcc.depart
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
              <CFormLabel class="col-sm-4 col-form-label">거래은행</CFormLabel>
              <CCol sm="8">
                <CFormSelect v-model.number="form.bankcode" required>
                  <option value="">---------</option>
                  <option
                    v-for="bank in bankCodeList"
                    :key="bank.pk"
                    :value="bank.pk"
                  >
                    {{ bank.name }}
                  </option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">관리부서</CFormLabel>
              <CCol sm="8">
                <CFormSelect v-model.number="form.depart">
                  <option value="">---------</option>
                  <option
                    v-for="dep in getSlugDeparts"
                    :key="dep.value"
                    :value="dep.value"
                  >
                    {{ dep.label }}
                  </option>
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
                <CFormInput
                  v-model="form.alias_name"
                  maxlength="20"
                  placeholder="계좌별칭"
                  required
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계좌번호
              </CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.number"
                  maxlength="30"
                  placeholder="계좌번호"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label"> 예금주</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.holder"
                  maxlength="20"
                  placeholder="예금주"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">개설일자</CFormLabel>
              <CCol sm="8">
                <DatePicker
                  v-model="form.open_date"
                  maxlength="10"
                  placeholder="개설일자"
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
                <CFormTextarea
                  v-model="form.note"
                  maxlength="50"
                  placeholder="비고"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label"></CFormLabel>
              <CCol sm="8">
                <v-switch
                  v-model="form.is_hide"
                  label="입출금 등록시 숨김"
                  color="indigo"
                  hide-details
                />
                <v-tooltip activator="parent" location="end">
                  입출금 등록 시 이 계좌 항목을 숨김.
                </v-tooltip>
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label"></CFormLabel>
              <CCol sm="8">
                <v-switch
                  v-model="form.inactive"
                  label="사용종료 계좌"
                  color="danger"
                  hide-details
                />
                <v-tooltip activator="parent" location="start">
                  해지된 계좌로 내역만 확인 가능.
                </v-tooltip>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol sm="12" class="text-right pt-1">
            <CButton color="success" type="submit" :disabled="formsCheck">
              거래 계좌 정보 저장하기
            </CButton>
          </CCol>
        </CRow>
      </div>
    </CModalBody>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header>거래계좌 정보 업데이트</template>
    <template #default> 거래계좌 정보를 업데이트하시겠습니까?</template>
    <template #footer>
      <CButton color="success" @click="onBankUpdate">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
