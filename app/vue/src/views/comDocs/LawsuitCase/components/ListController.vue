<script lang="ts" setup>
import { reactive, computed, nextTick, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { SuitCaseFilter, useDocument } from '@/store/pinia/document'
import { numFormat } from '@/utils/baseMixins'

defineProps({ tab: { type: Number, default: null } })
const emit = defineEmits(['docs-filter'])

const form = reactive<SuitCaseFilter>({
  page: 1,
  is_com: false,
  project: null,
  sort: '',
  level: '',
  court: '',
})

const formsCheck = computed(() => {
  const a = form.is_com === false
  const b = form.project === null
  const c = form.sort === ''
  const d = form.level === ''
  const e = form.court === ''
  return a && b && c && d && e
})

const documentStore = useDocument()
const suitcaseCount = computed(() => documentStore.suitcaseCount)

const listFiltering = (page = 1) => {
  nextTick(() => {
    // form.is_com = form.project === 'com'
    emit('docs-filter', {
      ...{ page },
      ...form,
    })
  })
}

defineExpose({ listFiltering })

const resetForm = () => {
  form.is_com = false
  form.project = null
  form.sort = ''
  form.level = ''
  form.court = ''
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
          <CCol md="6" lg="5" xl="4" class="mb-3">
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

          <CCol md="6" lg="5" xl="4" class="mb-3">
            <CFormSelect v-model="form.sort" @change="listFiltering(1)">
              <option value="">사건유형 선택</option>
              <option value="1">민사</option>
              <option value="2">형사</option>
              <option value="3">행정</option>
              <option value="4">가사</option>
              <option value="5">신청/집행</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="5" xl="4" class="mb-3">
            <CFormSelect v-model="form.sort" @change="listFiltering(1)">
              <option value="">사건심급 선택</option>
              <option value="1">1심</option>
              <option value="2">2심</option>
              <option value="3">3심</option>
              <option value="0">신청/집행</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="6">
        <CRow class="justify-content-md-end">
          <!--          <CCol md="6" lg="5" xl="4" class="mb-3">-->
          <!--            <CFormSelect>-->
          <!--              <option value="">제목+내용+작성자</option>-->
          <!--            </CFormSelect>-->
          <!--          </CCol>-->

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
        <strong>
          문서 건수 조회 결과 : {{ numFormat(suitcaseCount, 0, 0) }} 건
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
