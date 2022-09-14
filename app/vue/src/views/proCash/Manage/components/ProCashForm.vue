<script lang="ts" setup>
import { ref, reactive, computed, watch, onBeforeMount, nextTick } from 'vue'
import { useProCash } from '@/store/pinia/proCash'
import { useAccount } from '@/store/pinia/account'
import { diffDate, dateFormat, cutString, numFormat } from '@/utils/baseMixins'
import { write_project_cash } from '@/utils/pageAuth'
import { ProjectCashBook, ProSepItems } from '@/store/types/proCash'
import { isValidate } from '@/utils/helper'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  proCash: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const sepItem = reactive<ProSepItems>({
  pk: null,
  project_account_d1: null,
  project_account_d2: null,
  is_imprest: false,
  content: '',
  trader: '',
  income: null,
  outlay: null,
  evidence: '',
  note: '',
})

const validated = ref(false)

const form = reactive<ProjectCashBook>({
  pk: null,
  project: null,
  sort: null,
  project_account_d1: null,
  project_account_d2: null,

  is_separate: false,
  separated: null as null | number,
  is_imprest: false,

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
  if (props.proCash) {
    const a = form.project === props.proCash.project
    const b = form.sort === props.proCash.sort
    const c = form.project_account_d1 === props.proCash.project_account_d1
    const d = form.project_account_d2 === props.proCash.project_account_d2
    const e = form.content === props.proCash.content
    const f = form.trader === props.proCash.trader
    const g = form.bank_account === props.proCash.bank_account
    const h = form.income === props.proCash.income
    const i = form.outlay === props.proCash.outlay
    const j = form.evidence === props.proCash.evidence
    const k = form.note === props.proCash.note
    const l = form.deal_date === props.proCash.deal_date
    const m = form.is_separate === props.proCash.is_separate

    return a && b && c && d && e && f && g && h && i && j && k && l && m
  } else return false
})

const proCashStore = useProCash()
const formAccD1List = computed(() => proCashStore.formAccD1List)
const formAccD2List = computed(() => proCashStore.formAccD2List)
const proBankAccountList = computed(() => proCashStore.proBankAccountList)

const fetchProFormAccD1List = (sort: number | null) =>
  proCashStore.fetchProFormAccD1List(sort)
const fetchProFormAccD2List = (d1: number | null, sort: number | null) =>
  proCashStore.fetchProFormAccD2List(d1, sort)

const requireItem = computed(
  () => !!form.project_account_d1 && !!form.project_account_d2,
)

const sepDisabled = computed(() => {
  const disabled = !!form.project_account_d1 || !!form.project_account_d2
  return props.proCash ? disabled || props.proCash.sepItems.length : disabled
})

const sepSummary = computed(() => {
  const inc =
    props.proCash.sepItems.length !== 0
      ? props.proCash.sepItems
          .map((s: ProjectCashBook) => s.income)
          .reduce((res: number, el: number) => res + el)
      : 0
  const out =
    props.proCash.sepItems.length !== 0
      ? props.proCash.sepItems
          .map((s: ProSepItems) => s.outlay)
          .reduce((res: number, el: number) => res + el)
      : 0
  return [inc, out]
})

const sepUpdate = (sep: ProjectCashBook) => {
  sepItem.pk = sep.pk
  sepItem.project_account_d1 = sep.project_account_d1
  sepItem.project_account_d2 = sep.project_account_d2
  sepItem.content = sep.content
  sepItem.trader = sep.trader
  sepItem.evidence = sep.evidence
  sepItem.outlay = sep.outlay
  sepItem.income = sep.income
  sepItem.note = sep.note
}

const sepRemove = () => {
  sepItem.pk = null
  sepItem.project_account_d1 = null
  sepItem.project_account_d2 = null
  sepItem.content = ''
  sepItem.trader = ''
  sepItem.evidence = ''
  sepItem.outlay = null
  sepItem.income = null
  sepItem.note = ''
}

const isModify = computed(() => {
  if (!form.is_separate) return !!props.proCash
  else return !!sepItem.pk
})

const callAccount = () => {
  nextTick(() => {
    const sort = form.sort
    const d1 = form.project_account_d1
    fetchProFormAccD1List(sort)
    fetchProFormAccD2List(d1, sort)
  })
}

const sort_change = (event: Event) => {
  const el = event.target as HTMLSelectElement
  if (el.value === '1') form.outlay = null
  if (el.value === '2') form.income = null
  if (el.value === '3') {
    form.project_account_d1 = 17
    form.project_account_d2 = 62
  } else {
    form.project_account_d1 = null
    form.project_account_d2 = null
  }
  callAccount()
}

const d1_change = () => {
  form.project_account_d2 = null
  callAccount()
}

const sepD1_change = () => {
  sepItem.project_account_d2 = null
  nextTick(() => {
    const sort = form.sort
    const d1 = sepItem.project_account_d1
    fetchProFormAccD1List(sort)
    fetchProFormAccD2List(d1, sort)
  })
}

watch(form, val => {
  if (val.project_account_d2 === 63) form.is_imprest = true
  else form.is_imprest = false
})

const accountStore = useAccount()
const allowedPeriod = computed(
  () => accountStore.superAuth || diffDate(props.proCash.deal_date) <= 30,
)

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    const payload = !form.is_separate
      ? { formData: form, sepData: null }
      : { formData: form, sepData: sepItem }

    if (write_project_cash) {
      if (props.proCash) {
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
  if (write_project_cash)
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
    project: props.proCash.project,
    pk: props.proCash.pk,
  })
  delModal.value.close()
  emit('close')
}

onBeforeMount(() => {
  if (props.proCash) {
    form.pk = props.proCash.pk
    form.project = props.proCash.project
    form.sort = props.proCash.sort
    form.project_account_d1 = props.proCash.project_account_d1
    form.project_account_d2 = props.proCash.project_account_d2
    form.content = props.proCash.content
    form.trader = props.proCash.trader
    form.bank_account = props.proCash.bank_account
    form.income = props.proCash.income
    form.outlay = props.proCash.outlay
    form.evidence = props.proCash.evidence
    form.note = props.proCash.note
    form.deal_date = props.proCash.deal_date
    form.is_separate = props.proCash.is_separate
    form.separated = props.proCash.separated
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
                  required
                  maxlength="10"
                  placeholder="거래일자"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model.number="form.sort"
                  required
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
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계정[상위분류]
              </CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model.number="form.project_account_d1"
                  :required="!form.is_separate"
                  :disabled="!form.sort || form.is_separate"
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
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계정[하위분류]
              </CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model.number="form.project_account_d2"
                  :required="!form.is_separate"
                  :disabled="!form.project_account_d1 || form.is_separate"
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
                  v-c-tooltip="{
                    content:
                      '분양대금(분담금) 수납 건인 경우 반드시 해당 계좌에 기재된 입금자를 기재',
                    placement: 'top',
                  }"
                  maxlength="20"
                  placeholder="거래처 (수납자)"
                  required
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
                {{ !proCash && form.sort === 3 ? '출금' : '거래' }}계좌
              </CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model.number="form.bank_account"
                  required
                  :disabled="!form.sort"
                >
                  <option value="">---------</option>
                  <option
                    v-for="ba in proBankAccountList"
                    :key="ba.pk"
                    :value="ba.pk"
                  >
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
                <CFormSelect
                  v-model="form.evidence"
                  :required="!form.is_separate"
                  :disabled="form.is_separate"
                >
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

            <CRow v-if="!proCash && form.sort === 3">
              <CFormLabel class="col-sm-4 col-form-label">입금계좌</CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model.number="form.bank_account_to"
                  required
                  :disabled="form.sort !== 3"
                >
                  <option value="">---------</option>
                  <option
                    v-for="ba in proBankAccountList"
                    :key="ba.pk"
                    :value="ba.pk"
                  >
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
        <hr v-if="proCash && proCash.sepItems.length > 0" />
        <CRow v-if="proCash && proCash.sepItems.length > 0" class="mb-3">
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

        <div v-if="proCash">
          <CRow
            v-for="(sep, i) in proCash.sepItems"
            :key="sep.pk"
            class="mb-1"
            :class="
              sep.pk === sepItem.pk
                ? 'text-success text-decoration-underline'
                : ''
            "
          >
            <CCol sm="1">{{ i + 1 }}</CCol>
            <CCol sm="2">{{ sep.trader }}</CCol>
            <CCol sm="5">{{ cutString(sep.content, 20) }}</CCol>
            <CCol sm="2" class="text-right">
              {{ sep.income ? numFormat(sep.income) : numFormat(sep.outlay) }}
            </CCol>
            <CCol sm="2" class="text-right">
              <CButton
                type="button"
                color="success"
                size="sm"
                @click="sepUpdate(sep)"
              >
                수정
              </CButton>
            </CCol>
          </CRow>
        </div>

        <hr />
        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    계정[상위분류]
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormSelect
                      v-model.number="sepItem.project_account_d1"
                      required
                      @change="sepD1_change"
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
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    계정[하위분류]
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormSelect
                      v-model.number="sepItem.project_account_d2"
                      :disabled="!sepItem.project_account_d1"
                      required
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
            </CRow>
          </CCol>
        </CRow>
        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    적요
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormInput
                      v-model="sepItem.content"
                      maxlength="50"
                      placeholder="거래 내용"
                    />
                  </CCol>
                </CRow>
              </CCol>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    거래처
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormInput
                      v-model="sepItem.trader"
                      v-c-tooltip="{
                        content:
                          '분양대금(분담금) 수납 건인 경우 반드시 해당 계좌에 기재된 입금자를 기재',
                        placement: 'top',
                      }"
                      maxlength="20"
                      placeholder="거래처 (수납자)"
                      required
                    />
                  </CCol>
                </CRow>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    거래계좌
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormSelect
                      v-model.number="sepItem.bank_account"
                      readonly
                      required
                      :disabled="sepItem.pk || form.is_separate"
                    >
                      <option value="">---------</option>
                      <option
                        v-for="ba in proBankAccountList"
                        :key="ba.pk"
                        :value="ba.pk"
                      >
                        {{ ba.alias_name }}
                      </option>
                    </CFormSelect>
                  </CCol>
                </CRow>
              </CCol>

              <CCol sm="6">
                <CRow v-if="form.sort === 2">
                  <CFormLabel class="col-sm-4 col-form-label">
                    지출증빙
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormSelect v-model="sepItem.evidence" required>
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
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    출금액
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormInput
                      v-model.number="sepItem.outlay"
                      type="number"
                      min="0"
                      placeholder="출금 금액"
                      :required="form.sort === 2"
                      :disabled="form.sort !== 2"
                    />
                  </CCol>
                </CRow>
              </CCol>

              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    입금액
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormInput
                      v-model.number="sepItem.income"
                      type="number"
                      min="0"
                      placeholder="입금 금액"
                      :required="form.sort === 1"
                      :disabled="form.sort !== 1"
                    />
                  </CCol>
                </CRow>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
              <CCol sm="10">
                <CFormTextarea v-model="sepItem.note" placeholder="특이사항" />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </div>
    </CModalBody>

    <CModalFooter>
      <CButton type="button" color="light" @click="emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          v-if="sepItem.pk"
          type="button"
          color="dark"
          variant="outline"
          @click="sepRemove"
        >
          취소
        </CButton>
        <CButton
          type="submit"
          :color="isModify ? 'success' : 'primary'"
          :disabled="formsCheck && requireItem"
        >
          저장
        </CButton>
        <CButton
          v-if="isModify"
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
      프로젝트 입출금 거래 정보 삭제
    </template>
    <template #default>
      삭제한 데이터는 복구할 수 없습니다. 해당 입출금 거래 정보를
      삭제하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
