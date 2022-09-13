<script lang="ts" setup>
import { ref, reactive, computed, nextTick, onBeforeMount, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { useComCash } from '@/store/pinia/comCash'
import { CashBook } from '@/store/types/comCash'
import { dateFormat, diffDate, cutString, numFormat } from '@/utils/baseMixins'
import { write_company_cash, write_project_cash } from '@/utils/pageAuth'
import DatePicker from '@/components/DatePicker/index.vue'
import { isValidate } from '@/utils/helper'

const props = defineProps({ cash: { type: Object, required: true } })
const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const sepItem = reactive<CashBook>({
  pk: null,
  company: null,
  sort: null,
  account_d1: null,
  account_d2: null,
  account_d3: null,

  is_separate: false,
  separated: null,

  content: '',
  trader: '',
  bank_account: null,
  income: null,
  outlay: null,
  evidence: '',
  note: '',
  deal_date: '',
})

const validated = ref(false)

const form = reactive<CashBook>({
  pk: null,
  company: null,
  sort: null,
  account_d1: null,
  account_d2: null,
  account_d3: null,

  is_separate: false,
  separated: null as null | number,

  content: '',
  trader: '',
  bank_account: null,
  income: null,
  outlay: null,
  evidence: '',
  note: '',
  deal_date: dateFormat(new Date()),
})

watch(form, val => {
  if (val.deal_date) form.deal_date = dateFormat(val.deal_date)
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
    const m = form.deal_date === props.cash.deal_date

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

const requireItem = computed(
  () => !!form.account_d1 && !!form.account_d2 && !!form.account_d3,
)

const sepDisabled = computed(() => {
  const disabled = !!form.account_d1 || !!form.account_d2 || !!form.account_d3
  return props.cash ? disabled || props.cash.sepItems.length : disabled
})

const sepSummary = computed(() => {
  const inc = props.cash.sepItems.length
    ? props.cash.sepItems
        .map((s: CashBook) => s.income)
        .reduce((res: number, el: number) => res + el)
    : 0
  const out =
    props.cash.sepItems.length !== 0
      ? props.cash.sepItems
          .map((s: CashBook) => s.outlay)
          .reduce((res: number, el: number) => res + el)
      : 0
  return [inc, out]
})

const sepUpdate = (sep: CashBook) => {
  sepItem.pk = sep.pk
  sepItem.account_d1 = sep.account_d1
  sepItem.account_d2 = sep.account_d2
  sepItem.account_d3 = sep.account_d3
  sepItem.content = sep.content
  sepItem.trader = sep.trader
  sepItem.evidence = sep.evidence
  sepItem.outlay = sep.outlay
  sepItem.income = sep.income
  sepItem.note = sep.note
}

const sepRemove = () => {
  sepItem.pk = null
  sepItem.account_d1 = null
  sepItem.account_d2 = null
  sepItem.account_d3 = null
  sepItem.content = ''
  sepItem.trader = ''
  sepItem.evidence = ''
  sepItem.outlay = null
  sepItem.income = null
  sepItem.note = ''
}

const isModify = computed(() => {
  if (!form.is_separate) return !!props.cash
  else return !!sepItem.pk
})

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

const accountStore = useAccount()
const allowedPeriod = computed(
  () => accountStore.superAuth || diffDate(props.cash.deal_date) <= 30,
)

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    if (form.is_separate) {
      sepItem.sort = form.sort
      sepItem.bank_account = form.bank_account
      sepItem.deal_date = form.deal_date
    }
    const payload = !form.is_separate
      ? { formData: form, sepData: null }
      : { formData: form, sepData: sepItem }

    if (write_company_cash) {
      if (props.cash) {
        if (allowedPeriod.value) emit('multi-submit', payload)
        else
          alertModal.value.callModal(
            null,
            '거래일로부터 30일이 경과한 건은 수정할 수 없습니다. 관리자에게 문의바랍니다.',
          )
      } else emit('multi-submit', payload)
    } else alertModal.value.callModal()
    emit('close')
  }
}

const deleteConfirm = () => {
  if (write_company_cash)
    if (allowedPeriod.value) delModal.value.callModal()
    else
      alertModal.value.callModal(
        null,
        '거래일로부터 30일이 경과한 건은 삭제할 수 없습니다. 관리자에게 문의바랍니다.',
      )
  else alertModal.value.callModal()
}

const deleteObject = () => {
  emit('on-delete', {
    project: props.cash.project,
    pk: props.cash.pk,
  })
  delModal.value.close()
  emit('close')
}

onBeforeMount(() => {
  if (props.cash) {
    sepItem.company = props.cash.company
    sepItem.sort = props.cash.sort
    sepItem.bank_account = props.cash.bank_account
    sepItem.deal_date = props.cash.deal_date
    sepItem.separated = props.cash.pk

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
    form.evidence = props.cash.evidence
    form.note = props.cash.note
    form.deal_date = props.cash.deal_date
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
      <div>
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
                  :disabled="cash && !!cash.sort"
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
                  :disabled="!form.sort"
                  @change="d1_change"
                >
                  <option value="">---------</option>
                  <option
                    v-for="d1 in formAccD1List"
                    :key="d1.pk"
                    :value="d1.pk"
                  >
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
                  :disabled="!form.account_d1"
                  @change="d2_change"
                >
                  <option value="">---------</option>
                  <option
                    v-for="d2 in formAccD2List"
                    :key="d2.pk"
                    :value="d2.pk"
                  >
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
                  :disabled="!form.account_d2"
                >
                  <option value="">---------</option>
                  <option
                    v-for="d3 in formAccD3List"
                    :key="d3.pk"
                    :value="d3.pk"
                  >
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
                  :disabled="!form.sort"
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
                  :disabled="!form.sort"
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
                  :disabled="!form.sort"
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
                  :disabled="form.sort === 1 || !form.sort"
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
                  :disabled="form.sort === 2 || !form.sort"
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
                  :disabled="!form.sort"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol class="text-medium-emphasis">
            <CFormCheck
              id="is_separate"
              v-model="form.is_separate"
              label="별도 분리기록 거래 건 - 여러 계정 항목이 1회에 입·출금되어 별도 분리 기록이 필요한 거래인 경우."
              :disabled="sepDisabled"
            />
          </CCol>
        </CRow>
      </div>

      <div v-if="form.is_separate">
        <hr v-if="cash && cash.sepItems.length > 0" />
        <CRow v-if="cash && cash.sepItems.length > 0" class="mb-3">
          <CCol>
            <strong>
              <CIcon name="cilDescription" class="mr-2" />
              {{
                sepSummary[0] ? `입금액 합계 : ${numFormat(sepSummary[0])}` : ''
              }}
              {{
                sepSummary[1] ? `출금액 합계 : ${numFormat(sepSummary[1])}` : ''
              }}
            </strong>
          </CCol>
        </CRow>

        <!--        <div v-if="cash">-->
        <!--          <CRow-->
        <!--            v-for="(sep, i) in cash.sepItems"-->
        <!--            :key="sep.pk"-->
        <!--            class="mb-1"-->
        <!--            :class="-->
        <!--              sep.pk === sepItem.pk-->
        <!--                ? 'text-success text-decoration-underline'-->
        <!--                : ''-->
        <!--            "-->
        <!--          >-->
        <!--            <CCol sm="1">{{ i + 1 }}</CCol>-->
        <!--            <CCol sm="2">{{ sep.trader }}</CCol>-->
        <!--            <CCol sm="5">{{ cutString(sep.content, 20) }}</CCol>-->
        <!--            <CCol sm="2" class="text-right">-->
        <!--              {{ sep.income ? numFormat(sep.income) : numFormat(sep.outlay) }}-->
        <!--            </CCol>-->
        <!--            <CCol sm="2" class="text-right">-->
        <!--              <CButton-->
        <!--                type="button"-->
        <!--                color="success"-->
        <!--                size="sm"-->
        <!--                @click="sepUpdate(sep)"-->
        <!--              >-->
        <!--                수정-->
        <!--              </CButton>-->
        <!--            </CCol>-->
        <!--          </CRow>-->
        <!--        </div>-->

        <hr />
        <!--        <CRow class="mb-3">-->
        <!--          <CCol sm="1"></CCol>-->
        <!--          <CCol sm="11">-->
        <!--            <CRow>-->
        <!--              <CCol sm="6">-->
        <!--                <CRow>-->
        <!--                  <CFormLabel class="col-sm-4 col-form-label">-->
        <!--                    계정[상위분류]-->
        <!--                  </CFormLabel>-->
        <!--                  <CCol sm="8">-->
        <!--                    <CFormSelect-->
        <!--                      v-model.number="sepItem.project_account_d1"-->
        <!--                      required-->
        <!--                      @change="sepD1_change"-->
        <!--                    >-->
        <!--                      <option value="">-&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;</option>-->
        <!--                      <option-->
        <!--                        v-for="d1 in formAccD1List"-->
        <!--                        :key="d1.pk"-->
        <!--                        :value="d1.pk"-->
        <!--                      >-->
        <!--                        {{ d1.name }}-->
        <!--                      </option>-->
        <!--                    </CFormSelect>-->
        <!--                  </CCol>-->
        <!--                </CRow>-->
        <!--              </CCol>-->
        <!--              <CCol sm="6">-->
        <!--                <CRow>-->
        <!--                  <CFormLabel class="col-sm-4 col-form-label">-->
        <!--                    계정[하위분류]-->
        <!--                  </CFormLabel>-->
        <!--                  <CCol sm="8">-->
        <!--                    <CFormSelect-->
        <!--                      v-model.number="sepItem.project_account_d2"-->
        <!--                      :disabled="!sepItem.project_account_d1"-->
        <!--                      required-->
        <!--                    >-->
        <!--                      <option value="">-&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;</option>-->
        <!--                      <option-->
        <!--                        v-for="d2 in formAccD2List"-->
        <!--                        :key="d2.pk"-->
        <!--                        :value="d2.pk"-->
        <!--                      >-->
        <!--                        {{ d2.name }}-->
        <!--                      </option>-->
        <!--                    </CFormSelect>-->
        <!--                  </CCol>-->
        <!--                </CRow>-->
        <!--              </CCol>-->
        <!--            </CRow>-->
        <!--          </CCol>-->
        <!--        </CRow>-->
        <!--        <CRow class="mb-3">-->
        <!--          <CCol sm="1"></CCol>-->
        <!--          <CCol sm="11">-->
        <!--            <CRow>-->
        <!--              <CCol sm="6">-->
        <!--                <CRow>-->
        <!--                  <CFormLabel class="col-sm-4 col-form-label">-->
        <!--                    적요-->
        <!--                  </CFormLabel>-->
        <!--                  <CCol sm="8">-->
        <!--                    <CFormInput-->
        <!--                      v-model="sepItem.content"-->
        <!--                      maxlength="50"-->
        <!--                      placeholder="거래 내용"-->
        <!--                    />-->
        <!--                  </CCol>-->
        <!--                </CRow>-->
        <!--              </CCol>-->
        <!--              <CCol sm="6">-->
        <!--                <CRow>-->
        <!--                  <CFormLabel class="col-sm-4 col-form-label">-->
        <!--                    거래처-->
        <!--                  </CFormLabel>-->
        <!--                  <CCol sm="8">-->
        <!--                    <CFormInput-->
        <!--                      v-model="sepItem.trader"-->
        <!--                      v-c-tooltip="{-->
        <!--                        content:-->
        <!--                          '분양대금(분담금) 수납 건인 경우 반드시 해당 계좌에 기재된 입금자를 기재',-->
        <!--                        placement: 'top',-->
        <!--                      }"-->
        <!--                      maxlength="20"-->
        <!--                      placeholder="거래처 (수납자)"-->
        <!--                      required-->
        <!--                    />-->
        <!--                  </CCol>-->
        <!--                </CRow>-->
        <!--              </CCol>-->
        <!--            </CRow>-->
        <!--          </CCol>-->
        <!--        </CRow>-->

        <!--        <CRow class="mb-3">-->
        <!--          <CCol sm="1"></CCol>-->
        <!--          <CCol sm="11">-->
        <!--            <CRow>-->
        <!--              <CCol sm="6">-->
        <!--                <CRow>-->
        <!--                  <CFormLabel class="col-sm-4 col-form-label">-->
        <!--                    거래계좌-->
        <!--                  </CFormLabel>-->
        <!--                  <CCol sm="8">-->
        <!--                    <CFormSelect-->
        <!--                      v-model.number="sepItem.bank_account"-->
        <!--                      readonly-->
        <!--                      required-->
        <!--                      :disabled="sepItem.pk"-->
        <!--                    >-->
        <!--                      <option value="">-&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;</option>-->
        <!--                      <option-->
        <!--                        v-for="ba in proBankAccountList"-->
        <!--                        :key="ba.pk"-->
        <!--                        :value="ba.pk"-->
        <!--                      >-->
        <!--                        {{ ba.alias_name }}-->
        <!--                      </option>-->
        <!--                    </CFormSelect>-->
        <!--                  </CCol>-->
        <!--                </CRow>-->
        <!--              </CCol>-->

        <!--              <CCol sm="6">-->
        <!--                <CRow v-if="form.sort === 2">-->
        <!--                  <CFormLabel class="col-sm-4 col-form-label">-->
        <!--                    지출증빙-->
        <!--                  </CFormLabel>-->
        <!--                  <CCol sm="8">-->
        <!--                    <CFormSelect v-model="sepItem.evidence" required>-->
        <!--                      <option value="">-&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;</option>-->
        <!--                      <option value="0">증빙 없음</option>-->
        <!--                      <option value="1">세금계산서</option>-->
        <!--                      <option value="2">계산서(면세)</option>-->
        <!--                      <option value="3">카드전표/현금영수증</option>-->
        <!--                      <option value="4">간이영수증</option>-->
        <!--                      <option value="5">거래명세서</option>-->
        <!--                      <option value="6">입금표</option>-->
        <!--                      <option value="7">지출결의서</option>-->
        <!--                    </CFormSelect>-->
        <!--                  </CCol>-->
        <!--                </CRow>-->
        <!--              </CCol>-->
        <!--            </CRow>-->
        <!--          </CCol>-->
        <!--        </CRow>-->

        <!--        <CRow class="mb-3">-->
        <!--          <CCol sm="1"></CCol>-->
        <!--          <CCol sm="11">-->
        <!--            <CRow>-->
        <!--              <CCol sm="6">-->
        <!--                <CRow>-->
        <!--                  <CFormLabel class="col-sm-4 col-form-label">-->
        <!--                    출금액-->
        <!--                  </CFormLabel>-->
        <!--                  <CCol sm="8">-->
        <!--                    <CFormInput-->
        <!--                      v-model.number="sepItem.outlay"-->
        <!--                      type="number"-->
        <!--                      min="0"-->
        <!--                      placeholder="출금 금액"-->
        <!--                      :required="form.sort === 2"-->
        <!--                      :disabled="form.sort !== 2"-->
        <!--                    />-->
        <!--                  </CCol>-->
        <!--                </CRow>-->
        <!--              </CCol>-->

        <!--              <CCol sm="6">-->
        <!--                <CRow>-->
        <!--                  <CFormLabel class="col-sm-4 col-form-label">-->
        <!--                    입금액-->
        <!--                  </CFormLabel>-->
        <!--                  <CCol sm="8">-->
        <!--                    <CFormInput-->
        <!--                      v-model.number="sepItem.income"-->
        <!--                      type="number"-->
        <!--                      min="0"-->
        <!--                      placeholder="입금 금액"-->
        <!--                      :required="form.sort === 1"-->
        <!--                      :disabled="form.sort !== 1"-->
        <!--                    />-->
        <!--                  </CCol>-->
        <!--                </CRow>-->
        <!--              </CCol>-->
        <!--            </CRow>-->
        <!--          </CCol>-->
        <!--        </CRow>-->

        <!--        <CRow class="mb-3">-->
        <!--          <CCol sm="1"></CCol>-->
        <!--          <CCol sm="11">-->
        <!--            <CRow>-->
        <!--              <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>-->
        <!--              <CCol sm="10">-->
        <!--                <CFormTextarea v-model="sepItem.note" placeholder="특이사항" />-->
        <!--              </CCol>-->
        <!--            </CRow>-->
        <!--          </CCol>-->
        <!--        </CRow>-->
      </div>
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
