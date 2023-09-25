<script lang="ts" setup>
import { ref, reactive, computed, onMounted, onUpdated, type PropType } from 'vue'
import { useRoute } from 'vue-router'
import { type SuitCase } from '@/store/types/document'
import { write_company_docs } from '@/utils/pageAuth'
import { courtChoices } from './components/court'
import Multiselect from '@vueform/multiselect'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  getSuitCase: { type: Object, required: true },
  suitcase: { type: Object as PropType<SuitCase | null>, default: null },
  viewRoute: { type: String, required: true },
})
const emit = defineEmits(['on-submit', 'close'])

const refDelModal = ref()
const refConfirmModal = ref()
const refAlertModal = ref()

const validated = ref(false)
const form = reactive<SuitCase>({
  pk: null,
  company: null,
  project: null,
  sort: '',
  level: '',
  related_case: null,
  court: '',
  other_agency: '',
  case_number: '',
  case_name: '',
  plaintiff: '',
  plaintiff_attorney: '',
  defendant: '',
  defendant_attorney: '',
  related_debtor: '',
  case_start_date: '',
  case_end_date: '',
  summary: '',
})

const formsCheck = computed(() => {
  if (props.suitcase) {
    const a = form.company === props.suitcase.company
    const b = form.project === props.suitcase.project
    const c = form.sort === props.suitcase.sort
    const d = form.level === props.suitcase.level
    const e = form.related_case === props.suitcase.related_case
    const f = form.court === props.suitcase.court
    const g = form.other_agency === props.suitcase.other_agency
    const h = form.case_number === props.suitcase.case_number
    const i = form.case_name === props.suitcase.case_name
    const j = form.plaintiff === props.suitcase.plaintiff
    const k = form.plaintiff_attorney === props.suitcase.plaintiff_attorney
    const l = form.defendant === props.suitcase.defendant
    const m = form.defendant_attorney === props.suitcase.defendant_attorney
    const n = form.related_debtor === props.suitcase.related_debtor
    const o = form.case_start_date === props.suitcase.case_start_date
    const p = form.case_end_date === props.suitcase.case_end_date
    const q = form.summary === props.suitcase.summary

    const group1 = a && b && c && d && e && f && g && h
    const group2 = i && j && k && l && m && n && o && p && q
    return group1 && group2
  } else return false
})

const sortName = computed(() =>
  props.suitcase && props.suitcase.project ? props.suitcase.proj_name : '본사',
)

const route = useRoute()
const btnClass = computed(() => (route.params.caseId ? 'success' : 'primary'))

const onSubmit = (event: Event) => {
  if (write_company_docs) {
    const el = event.currentTarget as HTMLFormElement
    if (!el.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else refConfirmModal.value.callModal()
  } else refAlertModal.value.callModal()
}

const modalAction = () => {
  emit('on-submit', { ...form })
  validated.value = false
  refConfirmModal.value.close()
}

const dataSetup = () => {
  if (props.suitcase) {
    form.pk = props.suitcase.pk
    form.company = props.suitcase.company
    form.project = props.suitcase.project
    form.sort = props.suitcase.sort
    form.level = props.suitcase.level
    form.related_case = props.suitcase.related_case
    form.court = props.suitcase.court
    form.other_agency = props.suitcase.other_agency
    form.case_number = props.suitcase.case_number
    form.case_name = props.suitcase.case_name
    form.plaintiff = props.suitcase.plaintiff
    form.plaintiff_attorney = props.suitcase.plaintiff_attorney
    form.defendant = props.suitcase.defendant
    form.defendant_attorney = props.suitcase.defendant_attorney
    form.related_debtor = props.suitcase.related_debtor
    form.case_start_date = props.suitcase.case_start_date
    form.case_end_date = props.suitcase.case_end_date
    form.summary = props.suitcase.summary
  }
}

onMounted(() => dataSetup())
onUpdated(() => dataSetup())
</script>

<template>
  <CRow class="mt-5">
    <CCol>
      <h5>
        {{ sortName }}
        <v-icon icon="mdi-chevron-double-right" size="xs" />
        소송 사건
      </h5>
    </CCol>
  </CRow>

  <hr />

  <CForm
    enctype="multipart/form-data"
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="mb-3">
      <CFormLabel for="sort" class="col-md-2 col-form-label">유형</CFormLabel>
      <CCol md="4">
        <CFormSelect id="sort" v-model="form.sort" required>
          <option value="">사건유형 선택</option>
          <option value="1">민사</option>
          <option value="2">형사</option>
          <option value="3">행정</option>
          <option value="4">신청</option>
          <option value="5">집행</option>
        </CFormSelect>
      </CCol>

      <CFormLabel for="level" class="col-md-2 col-form-label">심급</CFormLabel>
      <CCol md="4">
        <CFormSelect id="level" v-model="form.level" required>
          <option value="">사건심급 선택</option>
          <option v-if="!form.sort || form.sort <= '3'" value="1">1심</option>
          <option v-if="!form.sort || form.sort <= '3'" value="2">2심</option>
          <option v-if="!form.sort || form.sort <= '3'" value="3">3심</option>
          <option v-if="!form.sort || form.sort === '2'" value="4">고소/수사</option>
          <option v-if="!form.sort || form.sort === '4'" value="5">신청</option>
          <option v-if="!form.sort || form.sort === '4'" value="6">항고/이의</option>
          <option v-if="!form.sort || form.sort === '5'" value="7">집행</option>
        </CFormSelect>
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="related_case" class="col-md-2 col-form-label"> 관련사건</CFormLabel>
      <CCol md="4">
        <Multiselect
          v-model="form.related_case"
          :options="getSuitCase"
          placeholder="관련 사건"
          autocomplete="label"
          :classes="{ search: 'form-control multiselect-search' }"
          :add-option-on="['enter', 'tab']"
          searchable
        />
        <small class="text-blue-grey-lighten-2">
          본안 사건인 경우 원심 사건, 신청/집행 사건인 경우 관련 본안 사건 지정
        </small>
      </CCol>
      <CFormLabel for="related_debtor" class="col-md-2 col-form-label"> 제3채무자</CFormLabel>
      <CCol md="4">
        <CFormInput id="related_debtor" v-model="form.related_debtor" placeholder="제3채무자" />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="related_case" class="col-md-2 col-form-label"> 법원명</CFormLabel>
      <CCol md="4">
        <Multiselect
          v-model="form.court"
          :options="courtChoices"
          placeholder="법원 선택"
          autocomplete="label"
          :classes="{ search: 'form-control multiselect-search' }"
          :attrs="form.court || form.other_agency ? {} : { required: true }"
          :add-option-on="['enter', 'tab']"
          searchable
        />
      </CCol>

      <CFormLabel for="other_agency" class="col-md-2 col-form-label"> 기타 처리기관</CFormLabel>
      <CCol md="4">
        <CFormInput id="other_agency" v-model="form.other_agency" placeholder="기타 처리기관" />
        <small class="text-blue-grey-lighten-2">
          사건 유형이 기소 전 형사 사건인 경우 해당 수사기관을 기재
        </small>
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="case_number" class="col-md-2 col-form-label"> 사건번호</CFormLabel>
      <CCol md="4">
        <CFormInput id="case_number" v-model="form.case_number" placeholder="사건번호" required />
      </CCol>

      <CFormLabel for="case_name" class="col-md-2 col-form-label"> 사건명</CFormLabel>
      <CCol md="4">
        <CFormInput id="case_name" v-model="form.case_name" placeholder="사건명" required />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="plaintiff" class="col-md-2 col-form-label"> 원고(신청인)</CFormLabel>
      <CCol md="4">
        <CFormInput id="plaintiff" v-model="form.plaintiff" placeholder="원고(신청인)" required />
      </CCol>

      <CFormLabel for="defendant" class="col-md-2 col-form-label"> 피고(피신청인)</CFormLabel>
      <CCol md="4">
        <CFormInput id="defendant" v-model="form.defendant" placeholder="피고(피신청인)" required />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="plaintiff_attorney" class="col-md-2 col-form-label">
        원고측 대리인
      </CFormLabel>
      <CCol md="4">
        <CFormInput
          id="plaintiff_attorney"
          v-model="form.plaintiff_attorney"
          placeholder="원고측 대리인"
        />
      </CCol>

      <CFormLabel for="defendant_attorney" class="col-md-2 col-form-label">
        피고측 대리인
      </CFormLabel>
      <CCol md="4">
        <CFormInput
          id="defendant_attorney"
          v-model="form.defendant_attorney"
          placeholder="피고측 대리인"
        />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="case_start_date" class="col-md-2 col-form-label"> 사건개시일</CFormLabel>
      <CCol md="4">
        <DatePicker id="case_start_date" v-model="form.case_start_date" placeholder="사건개시일" />
      </CCol>

      <CFormLabel for="case_end_date" class="col-md-2 col-form-label"> 사건종결일</CFormLabel>
      <CCol md="4">
        <DatePicker id="case_end_date" v-model="form.case_end_date" placeholder="사건종결일" />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="summary" class="col-md-2 col-form-label"> 개요 및 경과</CFormLabel>
      <CCol>
        <CFormTextarea id="summary" v-model="form.summary" rows="4" placeholder="개요 및 경과" />
      </CCol>
    </CRow>

    <CRow>
      <CCol class="text-right">
        <CButton color="light" @click="$router.push({ name: `${viewRoute}` })"> 목록으로</CButton>
        <CButton v-if="route.params.caseId" color="light" @click="$router.go(-1)"> 뒤로</CButton>
        <CButton :color="btnClass" type="submit" :disabled="formsCheck"> 저장하기</CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="refDelModal">
    <template #header> {{ viewRoute }}</template>
    <template #default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template #footer>
      <CButton color="danger" disabled>삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="refConfirmModal">
    <template #header> {{ viewRoute }}</template>
    <template #default> {{ viewRoute }} 저장을 진행하시겠습니까?</template>
    <template #footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="refAlertModal" />
</template>
