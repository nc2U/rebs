<script lang="ts" setup>
import { ref, reactive, computed, nextTick, watch, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useAccount } from '@/store/pinia/account'
import { dateFormat, diffDate } from '@/utils/baseMixins'
import { write_project_cash } from '@/utils/pageAuth'
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

const sepPk = ref(null)
let sepItem = reactive({
  project: '',
  sort: '',
  project_account_d1: '',
  project_account_d2: '',
  content: '',
  trader: '',
  bank_account: '',
  income: null,
  outlay: null,
  evidence: '',
  note: '',
  deal_date: '',
  is_separate: false,
  separated: null,
  is_imprest: true,
})

if (props.imprest) {
  // eslint-disable-next-line vue/no-setup-props-destructure
  sepItem.project = props.imprest.project
  // eslint-disable-next-line vue/no-setup-props-destructure
  sepItem.sort = props.imprest.sort
  // eslint-disable-next-line vue/no-setup-props-destructure
  sepItem.bank_account = props.imprest.bank_account
  // eslint-disable-next-line vue/no-setup-props-destructure
  sepItem.deal_date = props.imprest.deal_date
  // eslint-disable-next-line vue/no-setup-props-destructure
  sepItem.separated = props.imprest.pk
}

const validated = ref(false)

const form = reactive<{
  project: string
  sort: string
  project_account_d1: string
  project_account_d2: string
  content: string
  trader: string
  bank_account: string
  income: null | string
  outlay: null | string
  evidence: string
  note: string
  deal_date: Date | string
  is_separate: boolean
  separated: null | string
  is_imprest: boolean
}>({
  project: '',
  sort: '',
  project_account_d1: '',
  project_account_d2: '',
  content: '',
  trader: '',
  bank_account: '',
  income: null,
  outlay: null,
  evidence: '',
  note: '',
  deal_date: new Date(),
  is_separate: false,
  separated: null,
  is_imprest: true,
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
    const l =
      form.deal_date.toString() === new Date(props.imprest.deal_date).toString()
    const m = form.is_separate === props.imprest.is_separate

    return a && b && c && d && e && f && g && h && i && j && k && l && m
  } else return false
})

const store = useStore()
const accountStore = useAccount()

const formAccD1List = computed(() => store.state.proCash.formAccD1List)
const formAccD2List = computed(() => store.state.proCash.formAccD2List)
const imprestBAccount = computed(() => store.getters['proCash/imprestBAccount'])

const fetchProFormAccD1List = (sort: string) =>
  store.dispatch('proCash/fetchProFormAccD1List', sort)
const fetchProFormAccD2List = (payload: { sort: string; d1: string }) =>
  store.dispatch('proCash/fetchProFormAccD2List', payload)

const requireItem = computed(() => {
  return form.project_account_d1 !== '' && form.project_account_d2 !== ''
})

const sepDisabled = computed(() => {
  const disabled =
    form.project_account_d1 !== '' || form.project_account_d2 !== ''
  return props.imprest
    ? disabled || props.imprest.sepItems.length > 0
    : disabled
})

const sepSummary = computed(() => {
  const inc =
    props.imprest.sepItems.length !== 0
      ? props.imprest.sepItems
          .map((s: any) => s.income)
          .reduce((res: any, el: any) => res + el)
      : 0
  const out =
    props.imprest.sepItems.length !== 0
      ? props.imprest.sepItems
          .map((s: any) => s.outlay)
          .reduce((res: any, el: any) => res + el)
      : 0
  return [inc, out]
})

const allowedPeriod = computed(() => {
  // 일반 사용자 편집 허용 기간(거래일 deal_date 로부터)
  return accountStore.superAuth || diffDate(props.imprest.deal_date) <= 30
})

const sort_change = (event: any) => {
  if (event.target.value === '1') form.outlay = null
  if (event.target.value === '2') form.income = null
  if (event.target.value === '3') {
    form.project_account_d1 = '17'
    form.project_account_d2 = '62'
  } else {
    form.project_account_d1 = ''
    form.project_account_d2 = ''
  }
  callAccount()
}
const d1_change = () => {
  form.project_account_d2 = ''
  callAccount()
}

const sepD1_change = () => {
  sepItem.project_account_d2 = ''
  nextTick(() => {
    const sort = form.sort
    const d1 = sepItem.project_account_d1
    fetchProFormAccD1List(sort)
    fetchProFormAccD2List({ sort, d1 })
  })
}

const callAccount = () => {
  nextTick(() => {
    const sort = form.sort
    const d1 = form.project_account_d1
    fetchProFormAccD1List(sort)
    fetchProFormAccD2List({ sort, d1 })
  })
}
const sepUpdate = (sep: any) => {
  sepPk.value = sep.pk
  sepItem.project_account_d1 = sep.project_account_d1
  sepItem.project_account_d2 = sep.project_account_d2
  sepItem.content = sep.content
  sepItem.trader = sep.trader
  sepItem.evidence = sep.evidence
  sepItem.outlay = sep.outlay
  sepItem.income = sep.income
  sepItem.note = sep.note
}

const createConfirm = (payload: any) => {
  if (write_project_cash) multiSubmit(payload)
  else alertModal.value.callModal()
}

const updateConfirm = (payload: any) => {
  if (write_project_cash)
    if (allowedPeriod.value) multiSubmit(payload)
    else
      alertModal.value.callModal(
        null,
        '거래일로부터 30일이 경과한 건은 수정할 수 없습니다. 관리자에게 문의바랍니다.',
      )
  else alertModal.value.callModal()
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

watch(form, val => {
  if (val.deal_date) form.deal_date = dateFormat(val.deal_date)
})

const onSubmit = (event: any) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    let formData = {}
    if (!formsCheck.value) {
      form.deal_date = dateFormat(form.deal_date)
      if (!props.imprest) formData = { ...form }
      else formData = { ...{ ...{ pk: props.imprest.pk }, ...form } }
    }
    let sepData = {}
    if (form.is_separate) {
      if (!sepPk.value) sepData = { ...sepItem }
      else sepData = { ...{ ...{ pk: sepPk.value }, ...sepItem } }
    }
    if (props.imprest || sepPk.value) updateConfirm({ formData, sepData })
    else createConfirm({ formData, sepData })
  }
}

const multiSubmit = (multiPayload: any) => {
  emit('multi-submit', multiPayload)
  emit('close')
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
    form.deal_date = new Date(props.imprest.deal_date)
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
                  placeholder="거래일자"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
              <CCol sm="8">
                <CFormSelect v-model="form.sort" required @change="sort_change">
                  <!--                  :disabled="imprest && imprest.sort !== ''"-->
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
                  v-model="form.project_account_d1"
                  :required="!form.is_separate"
                  :disabled="form.sort === '' || form.is_separate"
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
                  v-model="form.project_account_d2"
                  :required="!form.is_separate"
                  :disabled="form.project_account_d1 === '' || form.is_separate"
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
                  placeholder="거래 내용"
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
                  v-c-tooltip="{
                    content:
                      '분양대금(분담금) 수납 건인 경우 반드시 해당 계좌에 기재된 입금자를 기재',
                    placement: 'top',
                  }"
                  placeholder="거래처 (수납자)"
                  required
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
                {{ !imprest && form.sort === '3' ? '출금' : '거래' }}계좌
              </CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model="form.bank_account"
                  required
                  :disabled="form.sort === ''"
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

            <CRow v-if="!imprest && form.sort === '3'">
              <CFormLabel class="col-sm-4 col-form-label">입금계좌</CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model="form.bank_account_to"
                  required
                  :disabled="form.sort !== '3'"
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

        <CRow>
          <CCol class="text-medium-emphasis">
            <CFormCheck
              v-model="form.is_separate"
              label="별도 분리기록 거래 건 - 여러 계정 항목이 1회에 입·출금되어 별도 분리 기록이 필요한 거래인 경우."
              :disabled="sepDisabled"
            />
          </CCol>
        </CRow>
      </div>

      <div v-if="form.is_separate && imprest">
        <hr v-if="imprest.sepItems.length > 0" />
        <CRow v-if="imprest.sepItems.length > 0" class="mb-3">
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

        <CRow
          v-for="(sep, i) in imprest.sepItems"
          :key="sep.pk"
          class="mb-1"
          :class="
            sep.pk === sepPk ? 'text-success text-decoration-underline' : ''
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
                      v-model="sepItem.project_account_d1"
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
                      v-model="sepItem.project_account_d2"
                      :disabled="sepItem.project_account_d1 === ''"
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
                      v-model="sepItem.bank_account"
                      readonly
                      required
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
                <CRow v-if="form.sort === '2'">
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
                      v-model="sepItem.outlay"
                      type="number"
                      min="0"
                      placeholder="출금 금액"
                      :required="form.sort === '2'"
                      :disabled="form.sort !== '2'"
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
                      v-model="sepItem.income"
                      type="number"
                      min="0"
                      placeholder="입금 금액"
                      :required="form.sort === '1'"
                      :disabled="form.sort !== '1'"
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
      <CButton type="button" color="light" @click="$emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          type="submit"
          :color="imprest ? 'success' : 'primary'"
          :disabled="formsCheck && requireItem"
        >
          저장
        </CButton>
        <CButton
          v-if="imprest"
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
