<script lang="ts" setup>
import { ref, computed, nextTick, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'

const props = defineProps({
  cash: {
    type: Object,
    required: true,
  },
})
const emit = defineEmits(['on-submit', 'on-delete', 'close'])

const validated = ref(false)

const form = ref({
  company: '',
  sort: '',
  account_d1: '',
  account_d2: '',
  account_d3: '',
  content: '',
  trader: '',
  bank_account: '',
  income: null,
  outlay: null,
  evidence: '',
  note: '',
  deal_date: new Date() as Date | string,
})

const formsCheck = computed(() => {
  if (props.cash) {
    const a = form.value.company === props.cash.company
    const b = form.value.sort === props.cash.sort
    const c = form.value.account_d1 === props.cash.account_d1
    const d = form.value.account_d2 === props.cash.account_d2
    const e = form.value.account_d3 === props.cash.account_d3
    const f = form.value.content === props.cash.content
    const g = form.value.trader === props.cash.trader
    const h = form.value.bank_account === props.cash.bank_account
    const i = form.value.income === props.cash.income
    const j = form.value.outlay === props.cash.outlay
    const k = form.value.evidence === props.cash.evidence
    const l = form.value.note === props.cash.note
    const m =
      form.value.deal_date.toString() ===
      new Date(props.cash.deal_date).toString()

    return a && b && c && d && e && f && g && h && i && j && k && l && m
  } else return false
})

const store = useStore()
const formAccD1List = computed(() => store.state.comCash.formAccD1List)
const formAccD2List = computed(() => store.state.comCash.formAccD2List)
const formAccD3List = computed(() => store.state.comCash.formAccD3List)
const comBankList = computed(() => store.state.comCash.comBankList)

const onSubmit = (event: any) => {
  const e = event.currentTarget
  if (e.checkValidity() === false) {
    event.preventDefault()
    event.stopPropagation()

    validated.value = true
  } else {
    form.value.deal_date = dateFormat(form.value.deal_date)
    emit('on-submit', form.value)
  }
}

const sort_change = (event: any) => {
  if (event.target.value === '1') {
    form.value.account_d1 = '4'
    form.value.account_d2 = ''
    form.value.account_d3 = ''
    form.value.outlay = null
  } else if (event.target.value === '2') {
    form.value.account_d1 = '5'
    form.value.account_d2 = ''
    form.value.account_d3 = ''
    form.value.income = null
  } else if (event.target.value === '3') {
    form.value.account_d1 = '6'
    form.value.account_d2 = '19'
    form.value.account_d3 = '128'
  } else {
    form.value.account_d1 = ''
    form.value.account_d2 = ''
    form.value.account_d3 = ''
  }
  callAccount()
}

const d1_change = () => {
  form.value.account_d2 = ''
  form.value.account_d3 = ''
  callAccount()
}

const d2_change = () => {
  form.value.account_d3 = ''
  callAccount()
}

const callAccount = () => {
  nextTick(() => {
    const sort = form.value.sort
    const d1 = form.value.account_d1 ? form.value.account_d1 : null
    const d2 = form.value.account_d2 ? form.value.account_d2 : null
    fetchFormAccD1List({ sort })
    fetchFormAccD2List({ sort, d1 })
    fetchFormAccD3List({ sort, d1, d2 })
  })
}
const fetchFormAccD1List = (payload: { sort: string }) =>
  store.dispatch('comCash/fetchFormAccD1List', payload)
const fetchFormAccD2List = (payload: { sort: string; d1: string | null }) =>
  store.dispatch('comCash/fetchFormAccD2List', payload)
const fetchFormAccD3List = (payload: {
  sort: string
  d1: string | null
  d2: string | null
}) => store.dispatch('comCash/fetchFormAccD3List', payload)

onBeforeMount(() => {
  if (props.cash) {
    form.value.company = props.cash.company
    form.value.sort = props.cash.sort
    form.value.account_d1 = props.cash.account_d1
    form.value.account_d2 = props.cash.account_d2
    form.value.account_d3 = props.cash.account_d3
    form.value.content = props.cash.content
    form.value.trader = props.cash.trader
    form.value.bank_account = props.cash.bank_account
    form.value.income = props.cash.income
    form.value.outlay = props.cash.outlay
    form.value.evidence = props.cash.evidence // ? cash.evidence : '0'
    form.value.note = props.cash.note
    form.value.deal_date = new Date(props.cash.deal_date)
  }
  callAccount()
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
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">거래일자</CFormLabel>
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

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.sort"
                required
                :disabled="cash && cash.sort !== ''"
                @change="sort_change"
              >
                <option value="">---------</option>
                <option value="1">입금</option>
                <option value="2">출금</option>
                <option value="3">대체</option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계정[대분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.account_d1"
                required
                :disabled="form.sort === ''"
                @change="d1_change"
              >
                <option value="">---------</option>
                <option v-for="d1 in formAccD1List" :key="d1.pk" :value="d1.pk">
                  {{ d1.name }}
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
              계정[중분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.account_d2"
                required
                :disabled="form.account_d1 === ''"
                @change="d2_change"
              >
                <option value="">---------</option>
                <option v-for="d2 in formAccD2List" :key="d2.pk" :value="d2.pk">
                  {{ d2.name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계정[소분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.account_d3"
                required
                :disabled="form.account_d2 === ''"
              >
                <option value="">---------</option>
                <option v-for="d3 in formAccD3List" :key="d3.pk" :value="d3.pk">
                  {{ d3.name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">적요</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.content"
                placeholder="거래 내용"
                required
                :disabled="form.sort === ''"
              />
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">거래처</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.trader"
                placeholder="거래처"
                :disabled="form.sort === ''"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              {{ !cash && form.sort === '3' ? '출금' : '거래' }}계좌
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.bank_account"
                required
                :disabled="form.sort === ''"
              >
                <option value="">---------</option>
                <option v-for="ba in comBankList" :key="ba.pk" :value="ba.pk">
                  {{ ba.alias_name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>

        <CCol sm="6">
          <CRow v-if="form.sort === '2'">
            <CFormLabel class="col-sm-4 col-form-label">지출증빙</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.evidence" required>
                <option value="">---------</option>
                <option value="0">증빙 없음</option>
                <option value="1">세금계산서</option>
                <option value="2">계산서(면세)</option>
                <option value="3">카드전표/현금영수증</option>
                <option value="4">간이영수증</option>
                <option value="5">거래명세서</option>
                <option value="6">입금표</option>
                <option value="7">지출결의서</option>
              </CFormSelect>
            </CCol>
          </CRow>

          <CRow v-if="!cash && form.sort === '3'">
            <CFormLabel class="col-sm-4 col-form-label">입금계좌</CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.bank_account_to"
                required
                :disabled="form.sort !== '3'"
              >
                <option value="">---------</option>
                <option v-for="ba in comBankList" :key="ba.pk" :value="ba.pk">
                  {{ ba.alias_name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">출금액</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model.number="form.outlay"
                type="number"
                min="0"
                placeholder="출금 금액"
                :required="form.sort === '2'"
                :disabled="form.sort === '1' || form.sort === ''"
              />
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">입금액</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model.number="form.income"
                type="number"
                min="0"
                placeholder="입금 금액"
                :required="form.sort === '1'"
                :disabled="form.sort === '2' || form.sort === ''"
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
                v-model.number="form.note"
                placeholder="특이사항"
                :disabled="form.sort === ''"
              />
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
          :color="cash ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="cash"
          type="button"
          color="danger"
          @click="emit('on-delete')"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>
  </CForm>
</template>
