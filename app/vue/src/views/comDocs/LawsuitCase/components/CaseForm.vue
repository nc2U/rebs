<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount, watch } from 'vue'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import { useDocument } from '@/store/pinia/document'
import { SuitCase } from '@/store/types/document'
import { write_company_docs } from '@/utils/pageAuth'
import { dateFormat } from '@/utils/baseMixins'
import { AlertSecondary } from '@/utils/cssMixins'
import ToastEditor from '@/components/ToastEditor/index.vue'
import FileUpload from '@/components/FileUpload.vue'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const emit = defineEmits(['on-submit', 'close'])

const delModal = ref()
const alertModal = ref()
const confirmModal = ref()

const form = reactive<SuitCase>({
  pk: null,
  project: null,
  sort: null,
  level: null,
  related_case: null,
  court: '',
  other_agency: '',
  case_number: '',
  case_name: '',
  plaintiff: '',
  defendant: '',
  related_debtor: '',
  case_start_date: '',
  summary: '',
})

const validated = ref(false)

const documentStore = useDocument()
const suitcase = computed(() => documentStore.suitcase)

const formsCheck = computed(() => {
  if (suitcase.value) {
    const a = form.project === suitcase.value.project
    const b = form.sort === suitcase.value.sort
    const c = form.level === suitcase.value.level
    const d = form.related_case === suitcase.value.related_case
    const e = form.court === suitcase.value.court
    const f = form.other_agency === suitcase.value.other_agency
    const g = form.case_number === suitcase.value.case_number
    const h = form.case_name === suitcase.value.case_name
    const i = form.plaintiff === suitcase.value.plaintiff
    const j = form.defendant === suitcase.value.defendant
    const k = form.related_debtor === suitcase.value.related_debtor
    const l = form.case_start_date === suitcase.value.case_start_date
    const m = form.summary === suitcase.value.summary

    const group1 = a && b && c && d && e && f && g
    const group2 = h && i && j && k && l && m
    return group1 && group2
  } else return false
})

const sortName = computed(() =>
  suitcase.value && suitcase.value.project ? suitcase.value.proj_name : '본사',
)

const fetchSuitCase = (pk: number) => documentStore.fetchSuitCase(pk)

const route = useRoute()
const btnClass = computed(() => (route.params.caseId ? 'success' : 'primary'))

const onSubmit = (event: Event) => {
  if (write_company_docs) {
    const el = event.currentTarget as HTMLFormElement
    if (!el.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else confirmModal.value.callModal()
  } else alertModal.value.callModal()
}

const modalAction = () => {
  emit('on-submit', { ...form })
  validated.value = false
  confirmModal.value.close()
}

const devideUri = (uri: string) => {
  const devidedUri = decodeURI(uri).split('media/')
  return [devidedUri[0] + 'media/', devidedUri[1]]
}

watch(form, val => {
  if (val.case_start_date)
    form.case_start_date = dateFormat(val.case_start_date)
})

watch(suitcase, val => {
  if (val) {
    form.pk = val.pk
    form.project = val.project
    form.sort = val.sort
    form.level = val.level
    form.related_case = val.related_case
    form.court = val.court
    form.other_agency = val.other_agency
    form.case_number = val.case_number
    form.case_name = val.case_name
    form.plaintiff = val.plaintiff
    form.defendant = val.defendant
    form.related_debtor = val.related_debtor
    form.case_start_date = val.case_start_date
    form.summary = val.summary
  }
})

watch(route, val => {
  if (val.params.caseId) fetchSuitCase(Number(val.params.caseId))
  else documentStore.suitcase = null
})

onBeforeMount(() => {
  if (route.params.caseId) fetchSuitCase(Number(route.params.caseId))
})

onBeforeRouteLeave(() => {
  documentStore.suitcase = null
})
</script>

<template>
  <CRow class="mt-5">
    <CCol>
      <h5>
        {{ sortName }}
        <v-icon icon="mdi-chevron-double-right" size="xs" />
        소송사건
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
      <CFormLabel for="title" class="col-md-2 col-form-label">유형</CFormLabel>
      <CCol md="6">
        <CFormInput
          id="title"
          v-model="form.sort"
          required
          placeholder="사건유형"
        />
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CFormLabel for="title" class="col-md-2 col-form-label">유형</CFormLabel>
      <CCol md="6">
        <CFormInput
          id="title"
          v-model="form.sort"
          required
          placeholder="사건유형"
        />
      </CCol>
    </CRow>

    <CRow>
      <CCol class="text-right">
        <CButton color="light" @click="$router.push({ name: '본사 소송사건' })">
          목록으로
        </CButton>
        <CButton
          v-if="route.params.caseId"
          color="light"
          @click="$router.go(-1)"
        >
          뒤로
        </CButton>
        <CButton :color="btnClass" type="submit" :disabled="formsCheck">
          저장하기
        </CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="delModal">
    <template #header>
      <CIcon name="cilChevronCircleRightAlt" />
      본사 소송사건
    </template>
    <template #default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template #footer>
      <CButton color="danger" disabled="">삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cilChevronCircleRightAlt" />
      본사 소송사건
    </template>
    <template #default> 본사 소송사건 저장을 진행하시겠습니까?</template>
    <template #footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
