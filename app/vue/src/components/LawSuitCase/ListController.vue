<script lang="ts" setup>
import { reactive, computed, nextTick, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { type SuitCaseFilter, useDocument } from '@/store/pinia/document'
import { numFormat } from '@/utils/baseMixins'
import { bgLight } from '@/utils/cssMixins'
import { courtChoices } from './components/court'
import Multiselect from '@vueform/multiselect'

const props = defineProps({
  comFrom: { type: Boolean, default: false },
  caseFilter: { type: Object, required: true },
})
const emit = defineEmits(['list-filter'])

const form = reactive<SuitCaseFilter>({
  company: '',
  project: '',
  is_com: props.comFrom,
  court: '',
  related_case: '',
  sort: '',
  level: '',
  in_progress: '',
  search: '',
  page: 1,
})

const formsCheck = computed(() => {
  const a = form.is_com === !!props.comFrom
  const b = !!props.comFrom ? form.project === '' : true
  const c = form.court === ''
  const d = form.related_case === ''
  const e = form.sort === ''
  const f = form.level === ''
  const g = form.in_progress === ''
  const h = form.search === ''
  return a && b && c && d && e && f && g && h
})

const projectStore = useProject()
const projSelect = computed(() => projectStore.projSelect)

const fetchProjectList = () => projectStore.fetchProjectList()

const documentStore = useDocument()
const suitcaseCount = computed(() => documentStore.suitcaseCount)
const getSuitCase = computed(() => documentStore.getSuitCase)

const listFiltering = (page = 1) => {
  nextTick(() => {
    form.page = page
    emit('list-filter', { ...form })
  })
}

const firstSorting = (event: { target: { value: number | null } }) => {
  const val = event.target.value
  if (!val) form.is_com = props.comFrom ?? true
  else {
    form.is_com = false
    form.project = val
  }
  listFiltering(1)
}

const courtChange = (court: string) => (form.court = court)
const searchChange = (search: string) => (form.search = search)
const relatedChange = (related: number) => (form.related_case = related)
const projectChange = (project: number | null) => (form.project = project ?? '')

defineExpose({
  listFiltering,
  courtChange,
  searchChange,
  relatedChange,
  projectChange,
})

const resetForm = () => {
  form.is_com = !!props.comFrom
  form.project = ''
  form.court = ''
  form.related_case = ''
  form.sort = ''
  form.level = ''
  form.in_progress = ''
  form.search = ''
  listFiltering(1)
}

const sortChange = () => {
  form.level = ''
  listFiltering(1)
}

onBeforeMount(() => {
  fetchProjectList()
  if (props.caseFilter) {
    form.company = props.caseFilter.company
    form.project = props.caseFilter.project
    form.court = props.caseFilter.court
    form.related_case = props.caseFilter.related_case
    form.sort = props.caseFilter.sort
    form.level = props.caseFilter.level
    form.in_progress = props.caseFilter.in_progress
    form.search = props.caseFilter.search
    form.page = props.caseFilter.page
  }
})
</script>

<template>
  <CCallout :color="comFrom ? 'primary' : 'success'" class="pb-0 mb-4" :class="bgLight">
    <CRow>
      <CCol :lg="comFrom ? 6 : 4">
        <CRow>
          <CCol v-if="comFrom" :md="comFrom ? 4 : 6" class="mb-3">
            <CFormSelect v-model="form.project" @change="firstSorting">
              <option value="">본사</option>
              <option v-for="proj in projSelect" :key="proj.value" :value="proj.value">
                {{ proj.label }}
              </option>
            </CFormSelect>
          </CCol>
          <CCol :md="comFrom ? 4 : 6" class="mb-3">
            <Multiselect
              v-model="form.court"
              :options="courtChoices"
              placeholder="관할법원"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter', 'tab']"
              searchable
              @change="listFiltering(1)"
            />
          </CCol>

          <CCol :md="comFrom ? 4 : 6" class="mb-3">
            <Multiselect
              v-model="form.related_case"
              :options="getSuitCase"
              placeholder="관련사건"
              autocomplete="label"
              :classes="{ search: 'form-control multiselect-search' }"
              :add-option-on="['enter', 'tab']"
              searchable
              @change="listFiltering(1)"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol :lg="comFrom ? 4 : 6">
        <CRow>
          <CCol md="4" class="mb-3">
            <CFormSelect v-model="form.sort" @change="sortChange">
              <option value="">사건유형 선택</option>
              <option value="1">민사</option>
              <option value="2">형사</option>
              <option value="3">행정</option>
              <option value="4">신청</option>
              <option value="5">집행</option>
            </CFormSelect>
          </CCol>
          <CCol md="4" class="mb-3">
            <CFormSelect v-model="form.level" @change="listFiltering(1)">
              <option value="">사건심급 선택</option>
              <option v-if="!form.sort || form.sort <= '3'" value="1">1심</option>
              <option v-if="!form.sort || form.sort <= '3'" value="2">2심</option>
              <option v-if="!form.sort || form.sort <= '3'" value="3">3심</option>
              <option v-if="!form.sort || form.sort === '2'" value="4">고소/수사</option>
              <option v-if="!form.sort || form.sort === '4'" value="5">신청</option>
              <option v-if="!form.sort || form.sort === '4'" value="6">항고/이의</option>
              <option v-if="!form.sort || form.sort === '5'" value="7">압류/추심</option>
              <option v-if="!form.sort || form.sort === '5'" value="8">정지/이의</option>
            </CFormSelect>
          </CCol>
          <CCol md="4" class="mb-3">
            <CFormSelect v-model="form.in_progress">
              <option value="">전체 사건</option>
              <option :value="true">진행 사건</option>
              <option :value="false">종결 사건</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="2">
        <CRow class="justify-content-md-end">
          <CCol lg="12" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="Search"
                @keydown.enter="listFiltering(1)"
              />
              <CInputGroupText @click="listFiltering(1)">검색</CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <CRow>
      <CCol color="warning" class="p-2 pl-3">
        <strong> 사건 수 조회 결과 : {{ numFormat(suitcaseCount, 0, 0) }} 건 </strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm"> 검색조건 초기화</CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
