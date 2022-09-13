<script lang="ts" setup>
import { ref, reactive, computed, nextTick, onBeforeMount } from 'vue'
import { useComCash } from '@/store/pinia/comCash'
import { CashBook } from '@/store/types/comCash'
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

const form = reactive<CashBook>({
  pk: null,
  company: null,
  sort: null,
  account_d1: null,
  account_d2: null,
  account_d3: null,
  content: '',
  trader: '',
  bank_account: null,
  income: null,
  outlay: null,
  evidence: '',
  note: '',
  deal_date: dateFormat(new Date()),
})

const formsCheck = computed(() => {
  if (props.cash) {
    const a = form.company === props.cash.company
    const b = form.sort === props.cash.sort
    const c = form.account_d1 === props.cash.account_d1
    const d = form.account_d2 === props.cash.account_d2
    const e = form.account_d3 === props.cash.account_d3
    const f = form.content === props.cash.content
    const g = form.trader === props.cash.trader
    const h = form.bank_account === props.cash.bank_account
    const i = form.income === props.cash.income
    const j = form.outlay === props.cash.outlay
    const k = form.evidence === props.cash.evidence
    const l = form.note === props.cash.note
    const m =
      form.deal_date.toString() === new Date(props.cash.deal_date).toString()

    return a && b && c && d && e && f && g && h && i && j && k && l && m
  } else return false
})

const useComCashStore = useComCash()
const formAccD1List = computed(() => useComCashStore.formAccD1List)
const formAccD2List = computed(() => useComCashStore.formAccD2List)
const formAccD3List = computed(() => useComCashStore.formAccD3List)
const comBankList = computed(() => useComCashStore.comBankList)

const fetchFormAccD1List = (sort: number | null) =>
  useComCashStore.fetchFormAccD1List(sort)
const fetchFormAccD2List = (sort: number | null, d1: number | null) =>
  useComCashStore.fetchFormAccD2List(sort, d1)
const fetchFormAccD3List = (
  sort: number | null,
  d1: number | null,
  d2: number | null,
) => useComCashStore.fetchFormAccD3List(sort, d1, d2)

const sort_change = (event: Event) => {
  if ((event.target as HTMLSelectElement).value === '1') {
    form.account_d1 = 4
    form.account_d2 = null
    form.account_d3 = null
    form.outlay = null
  } else if ((event.target as HTMLSelectElement).value === '2') {
    form.account_d1 = 5
    form.account_d2 = null
    form.account_d3 = null
    form.income = null
  } else if ((event.target as HTMLSelectElement).value === '3') {
    form.account_d1 = 6
    form.account_d2 = 19
    form.account_d3 = 128
  } else {
    form.account_d1 = null
    form.account_d2 = null
    form.account_d3 = null
  }
  callAccount()
}

const d1_change = () => {
  form.account_d2 = null
  form.account_d3 = null
  callAccount()
}

const d2_change = () => {
  form.account_d3 = null
  callAccount()
}

const callAccount = () => {
  nextTick(() => {
    const sort = form.sort
    const d1 = form.account_d1 ? form.account_d1 : null
    const d2 = form.account_d2 ? form.account_d2 : null
    fetchFormAccD1List(sort)
    fetchFormAccD2List(sort, d1)
    fetchFormAccD3List(sort, d1, d2)
  })
}

const onSubmit = (event: Event) => {
  const e = event.currentTarget as HTMLSelectElement
  if (!e.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()

    validated.value = true
  } else {
    form.deal_date = dateFormat(form.deal_date)
    emit('on-submit', { ...form })
    emit('close')
  }
}

onBeforeMount(() => {
  if (props.cash) {
    form.pk = props.cash.pk
    form.company = props.cash.company
    form.sort = props.cash.sort
    form.account_d1 = props.cash.account_d1
    form.account_d2 = props.cash.account_d2
    form.account_d3 = props.cash.account_d3
    form.content = props.cash.content
    form.trader = props.cash.trader
    form.bank_account = props.cash.bank_account
    form.income = props.cash.income
    form.outlay = props.cash.outlay
    form.evidence = props.cash.evidence // ? cash.evidence : '0'
    form.note = props.cash.note
    form.deal_date = dateFormat(new Date(props.cash.deal_date))
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
                maxlength="10"
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
                v-model.number="form.sort"
                required
                :disabled="cash && cash.sort !== null"
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
                v-model.number="form.account_d1"
                required
                :disabled="form.sort === null"
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
                v-model.number="form.account_d2"
                required
                :disabled="form.account_d1 === null"
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
                v-model.number="form.account_d3"
                required
                :disabled="form.account_d2 === null"
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
                maxlength="50"
                placeholder="거래 내용"
                required
                :disabled="form.sort === null"
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
                maxlength="20"
                placeholder="거래처"
                :disabled="form.sort === null"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              {{ !cash && form.sort === 3 ? '출금' : '거래' }}계좌
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model.number="form.bank_account"
                required
                :disabled="form.sort === null"
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
          <CRow v-if="form.sort === 2">
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

          <CRow v-if="!cash && form.sort === 3">
            <CFormLabel class="col-sm-4 col-form-label">입금계좌</CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.bank_account_to"
                required
                :disabled="form.sort !== 3"
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
                :required="form.sort === 2"
                :disabled="form.sort === 1 || form.sort === null"
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
                :required="form.sort === 1"
                :disabled="form.sort === 2 || form.sort === null"
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
                :disabled="form.sort === null"
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
