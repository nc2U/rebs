<script lang="ts" setup>
import { reactive, computed, nextTick, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { type PostFilter, useDocument } from '@/store/pinia/document'
import { numFormat } from '@/utils/baseMixins'
import { bgLight } from '@/utils/cssMixins'

const props = defineProps({
  tab: { type: Number, default: null },
  comFrom: { type: Boolean, default: false },
})
const emit = defineEmits(['list-filter'])

const form = reactive<PostFilter>({
  company: '',
  project: '',
  is_com: 'unknown',
  ordering: '-created',
  search: '',
})

const formsCheck = computed(() => {
  const a = form.company === ''
  const b = form.project === ''
  const c = form.is_com === false
  const d = form.ordering === '-created'
  const e = form.search === ''
  return a && b && c && d && e
})

const documentStore = useDocument()
const postCount = computed(() => documentStore.postCount)

const listFiltering = (page = 1) => {
  nextTick(() => {
    emit('list-filter', {
      ...{ page },
      ...form,
    })
  })
}

const firstSorting = (event: { target: { value: 'is_com' | number | null } }) => {
  const val = event.target.value
  if (val === null) form.is_com = 'unknown'
  else if (val === 'is_com') {
    form.is_com = true
    form.project = ''
  } else {
    form.is_com = false
    form.project = val
  }
  listFiltering(1)
}

const projectChange = (project: number | null) => {
  if (!!project) form.project = project
}

defineExpose({ listFiltering, projectChange })

const resetForm = () => {
  form.company = ''
  form.project = ''
  form.is_com = false
  form.ordering = '-created'
  form.search = ''
  listFiltering(1)
}

const projectStore = useProject()
const projSelect = computed(() => projectStore.projSelect)
const fetchProjectList = () => projectStore.fetchProjectList()
onBeforeMount(() => fetchProjectList())
</script>

<template>
  <CCallout :color="comFrom ? 'primary' : 'success'" class="pb-0 mb-4" :class="bgLight">
    <CRow>
      <CCol lg="6">
        <CRow>
          <CCol v-if="comFrom" md="6" lg="5" xl="4" class="mb-3">
            <CFormSelect v-model="form.project" @change="firstSorting">
              <option value="">전체 프로젝트</option>
              <option value="is_com">본사</option>
              <option v-for="proj in projSelect" :key="proj.value" :value="proj.value">
                {{ proj.label }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="5" xl="4" class="mb-3">
            <CFormSelect v-model="form.ordering" @change="listFiltering(1)">
              <option value="created">작성일자 오름차순</option>
              <option value="-created">작성일자 내림차순</option>
              <option value="execution_date">시행일자 오름차순</option>
              <option value="-execution_date">시행일자 내림차순</option>
              <option value="-hit">조회수 오름차순</option>
              <option value="hit">조회수 내림차순</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="6">
        <CRow class="justify-content-md-end">
          <CCol md="6" lg="5" xl="4" class="mb-3">
            <CFormSelect>
              <option value="">제목+내용+작성자</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="5" class="mb-3">
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
        <strong> 문서 건수 조회 결과 : {{ numFormat(postCount, 0, 0) }} 건 </strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm"> 검색조건 초기화</CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
