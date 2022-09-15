<script lang="ts" setup>
import { reactive, computed, nextTick } from 'vue'
import { useDocument } from '@/store/pinia/document'
import { numFormat } from '@/utils/baseMixins'

defineProps({ tab: { type: Number, default: null } })
const emit = defineEmits(['docs-filtering'])

const form = reactive({
  ordering: '-created_at',
  searchFilter: '',
  search: '',
})

const formsCheck = computed(() => {
  const a = form.ordering === '-created_at'
  const b = form.searchFilter === ''
  const c = form.search === ''
  return a && b && c
})

// const orderGroupList = computed(() => contractStore.orderGroupList)
// const contractsCount = computed(() => contractStore.contractsCount)
// const buildingList = computed(() => projectDataStore.buildingList)
// const simpleTypes = computed(() => projectDataStore.simpleTypes)
//
// watch(form, val => {
//   if (val.from_date) form.from_date = dateFormat(val.from_date)
//   else form.from_date = ''
//   if (val.to_date) form.to_date = dateFormat(val.to_date)
//   else form.to_date = ''
//   listFiltering(1)
// })

const documentStore = useDocument()
const postCount = computed(() => documentStore.postCount)

const listFiltering = (page = 1) => {
  nextTick(() => {
    emit('docs-filtering', {
      ...{ page },
      ...form,
    })
  })
}

defineExpose({ listFiltering })

const resetForm = () => {
  form.ordering = '-created_at'
  form.searchFilter = ''
  form.search = ''
  listFiltering(1)
}
</script>

<template>
  <CCallout color="primary" class="pb-0 mb-4">
    <CRow>
      <CCol lg="6">
        <CRow>
          <CCol md="4" lg="6" xl="3" class="mb-3">
            <CFormSelect v-model="form.ordering" @change="listFiltering(1)">
              <option value="-created_at">전체 프로젝트</option>
              <option value="created_at">본사</option>
              <option value="-contractor">(가칭)송도센트럴자이</option>
              <option value="-contractor">(가칭)아야진프로젝트</option>
            </CFormSelect>
          </CCol>

          <CCol md="4" lg="6" xl="3" class="mb-3">
            <CFormSelect v-model="form.ordering" @change="listFiltering(1)">
              <option value="-created_at">작성일자순</option>
              <option value="created_at">시행일자순</option>
              <option value="-contractor">조회수순</option>
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
