<script lang="ts" setup>
import { ref, reactive, computed, nextTick, watch, onBeforeMount } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { useProCash } from '@/store/pinia/proCash'
import { dateFormat, diffDate, numFormat, cutString } from '@/utils/baseMixins'
import { write_project_cash } from '@/utils/pageAuth'
import { ProjectCashBook } from '@/store/types/proCash'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { isValidate } from '@/utils/helper'

const props = defineProps({
  imprest: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

// const sepPk = ref<number | null>(null)
let sepItem = reactive<ProjectCashBook>({
  pk: null,
  project: null,
  sort: null,
  project_account_d1: null,
  project_account_d2: null,

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
  is_imprest: true,
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
  is_imprest: true,

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
  if (props.imprest) {
    const a = form.project === props.imprest.project
    const b = form.sort === props.imprest.sort
    const c = form.project_account_d1 === props.imprest.project_account_d1
    const d = form.project_account_d2 === props.imprest.project_account_d2
    const e = form.content === props.imprest.content
    const f = form.trader === props.imprest.trader
    const g = form.bank_account === props.imprest.bank_account
    const h = form.income === props.imprest.income
    const i = form.outlay === props.imprest.outlay
    const j = form.evidence === props.imprest.evidence
    const k = form.note === props.imprest.note
    const l = form.deal_date === props.imprest.deal_date
    const m = form.is_separate === props.imprest.is_separate

    return a && b && c && d && e && f && g && h && i && j && k && l && m
  } else return false
})

const proCashStore = useProCash()
const formAccD1List = computed(() => proCashStore.formAccD1List)
const formAccD2List = computed(() => proCashStore.formAccD2List)
const imprestBAccount = computed(() => proCashStore.imprestBAccount)

const fetchProFormAccD1List = (sort: number | null) =>
  proCashStore.fetchProFormAccD1List(sort)
const fetchProFormAccD2List = (d1: number | null, sort: number | null) =>
  proCashStore.fetchProFormAccD2List(d1, sort)

const requireItem = computed(
  () => !!form.project_account_d1 && !!form.project_account_d2,
)

const sepDisabled = computed(() => {
  const disabled = !!form.project_account_d1 || !!form.project_account_d2
  return props.imprest
    ? disabled || props.imprest.sepItems.length > 0
    : disabled
})

const sepSummary = computed(() => {
  const inc =
    props.imprest.sepItems.length !== 0
      ? props.imprest.sepItems
          .map((s: ProjectCashBook) => s.income || 0)
          .reduce((res: number, el: number) => res + el, 0)
      : 0
  const out =
    props.imprest.sepItems.length !== 0
      ? props.imprest.sepItems
          .map((s: ProjectCashBook) => s.outlay || 0)
          .reduce((res: number, el: number) => res + el, 0)
      : 0
  return [inc, out]
})

const accountStore = useAccount()
const allowedPeriod = computed(
  () =>
    // 일반 사용자 편집 허용 기간(거래일 deal_date 로부터)
    accountStore.superAuth || diffDate(props.imprest.deal_date) <= 30,
)

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

const callAccount = () => {
  nextTick(() => {
    const sort = form.sort
    const d1 = sepItem.project_account_d1
    fetchProFormAccD1List(sort)
    fetchProFormAccD2List(d1, sort)
  })
}

const sepUpdate = (sep: ProjectCashBook) => {
  // sepPk.value = sep.pk
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
  if (!form.is_separate) return !!props.imprest
  else return !!sepItem.pk
})

watch(form, val => {
  if (val.deal_date) form.deal_date = dateFormat(val.deal_date)
})

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    const payload = !form.is_separate
      ? { formData: form, sepData: null }
      : { formData: form, sepData: sepItem }

    if (write_project_cash) {
      if (props.imprest) {
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
    project: props.imprest.project,
    pk: props.imprest.pk,
  })
  delModal.value.visible = false
  emit('close')
}

onBeforeMount(() => {
  if (props.imprest) {
    sepItem.project = props.imprest.project
    sepItem.sort = props.imprest.sort
    sepItem.bank_account = props.imprest.bank_account
    sepItem.deal_date = props.imprest.deal_date
    sepItem.separated = props.imprest.pk

    form.pk = props.imprest.pk
    form.project = props.imprest.project
    form.sort = props.imprest.sort
    form.project_account_d1 = props.imprest.project_account_d1
    form.project_account_d2 = props.imprest.project_account_d2
    form.content = props.imprest.content
    form.trader = props.imprest.trader
    form.bank_account = props.imprest.bank_account
    form.income = props.imprest.income
    form.outlay = props.imprest.outlay
    form.evidence = props.imprest.evidence
    form.note = props.imprest.note
    form.deal_date = props.imprest.deal_date
    form.is_separate = props.imprest.is_separate
    form.separated = props.imprest.separated
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
                {{ !imprest && form.sort === 3 ? '출금' : '거래' }}계좌
              </CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model.number="form.bank_account"
                  required
                  :disabled="!form.sort"
                >
                  <option value="">---------</option>
                  <option
                    v-for="ba in imprestBAccount"
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

            <CRow v-if="!imprest && form.sort === 3">
              <CFormLabel class="col-sm-4 col-form-label">입금계좌</CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model.number="form.bank_account_to"
                  required
                  :disabled="form.sort !== 3"
                >
                  <option value="">---------</option>
                  <option
                    v-for="ba in imprestBAccount"
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
        <hr v-if="imprest && imprest.sepItems.length > 0" />
        <CRow v-if="imprest && imprest.sepItems.length > 0" class="mb-3">
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

        <div v-if="imprest">
          <CRow
            v-for="(sep, i) in imprest.sepItems"
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
                      :disabled="sepItem.pk"
                    >
                      <option value="">---------</option>
                      <option
                        v-for="ba in imprestBAccount"
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
      운영비(전도금) 거래 정보 삭제
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
