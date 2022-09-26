<script lang="ts" setup>
import { reactive, computed, nextTick, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { PostFilter, useDocument } from '@/store/pinia/document'
import { numFormat } from '@/utils/baseMixins'

defineProps({ tab: { type: Number, default: null } })
const emit = defineEmits(['docs-filter'])

const form = reactive<PostFilter>({
  is_com: false,
  project: '',
  ordering: '-created',
  search: '',
})

const formsCheck = computed(() => {
  const a = form.project === ''
  const b = form.is_com === false
  const c = form.ordering === '-created'
  const d = form.search === ''
  return a && b && c && d
})

const documentStore = useDocument()
const postCount = computed(() => documentStore.postCount)

const listFiltering = (page = 1) => {
  nextTick(() => {
    form.is_com = form.project === 'com'
    emit('docs-filter', {
      ...{ page },
      ...form,
    })
  })
}

defineExpose({ listFiltering })

const resetForm = () => {
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
  <CCallout color="primary" class="pb-0 mb-4">
    <CRow>
      <CCol lg="6">
        <CRow>
          <CCol md="4" lg="6" xl="3" class="mb-3">
            <CFormSelect v-model="form.project" @change="listFiltering(1)">
              <option value="">전체 프로젝트</option>
              <option value="com">본사</option>
              <option
                v-for="proj in projSelect"
                :key="proj.value"
                :value="proj.value"
              >
                {{ proj.text }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="4" lg="6" xl="3" class="mb-3">
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
          <CCol md="4" lg="6" xl="3" class="mb-3">
            <CFormSelect v-model="form.searchFilter" @change="listFiltering(1)">
              <option value="">전체</option>
              <option value="">제목+내용</option>
              <option value="">제목</option>
              <option value="">내용</option>
              <option value="">작성자</option>
            </CFormSelect>
          </CCol>

          <CCol md="4" lg="6" xl="4" class="mb-3">
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
        <strong>
          문서 건수 조회 결과 : {{ numFormat(postCount, 0, 0) }} 건
        </strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
