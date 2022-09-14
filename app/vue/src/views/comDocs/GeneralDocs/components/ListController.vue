<script lang="ts" setup>
import { reactive, computed, watch, nextTick } from 'vue'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'

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
//
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
  <CCallout color="info" class="pb-0 mb-4">
    <CRow>
      <CCol lg="12">
        <CRow>
          <CCol md="4" lg="6" xl="4" class="mb-3">
            <CFormSelect v-model="form.ordering" @change="listFiltering(1)">
              <option value="-created_at">정렬하기</option>
              <option value="-created_at">등록일시 내림차순</option>
              <option value="created_at">등록일시 올림차순</option>
              <option value="-contractor__contract_date">
                계약일자 내림차순
              </option>
              <option value="contractor__contract_date">
                계약일자 올림차순
              </option>
              <option value="-serial_number">일련번호 내림차순</option>
              <option value="serial_number">일련번호 올림차순</option>
              <option value="-contractor__name">계약자명 내림차순</option>
              <option value="contractor__name">계약자명 올림차순</option>
            </CFormSelect>
          </CCol>

          <CCol md="4" lg="6" xl="4" class="mb-3">
            <CFormSelect v-model="form.searchFilter" @change="listFiltering(1)">
              <option value="">제목+내용</option>
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
        <strong>계약 건수 조회 결과 : {{ 'docsCount' }} 건</strong>
      </CCol>
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
