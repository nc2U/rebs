<script setup lang="ts">
import { useDocument } from '@/store/pinia/document'
import Case from './Case.vue'
import Pagination from '@/components/Pagination'

defineProps({
  page: { type: Number, default: 1 },
  caseList: { type: Array, default: () => [] },
})

const emit = defineEmits(['page-select'])

const documentStore = useDocument()

const postCases = (num: number) => documentStore.postCases(num)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive align="middle" class="mt-5">
    <colgroup>
      <col width="7%" />
      <col width="7%" />
      <col width="23%" />
      <col width="27%" />
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="headerSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">구분</CTableHeaderCell>
        <CTableHeaderCell scope="col">심급</CTableHeaderCell>
        <CTableHeaderCell scope="col">관련사건</CTableHeaderCell>
        <CTableHeaderCell scope="col">사건명</CTableHeaderCell>
        <CTableHeaderCell scope="col">원고/신청인</CTableHeaderCell>
        <CTableHeaderCell scope="col">피고/피신청인</CTableHeaderCell>
        <CTableHeaderCell scope="col">제3채무자</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Case
        v-for="suitcase in caseList"
        :key="suitcase.pk"
        :suit-case="suitcase"
      />
    </CTableBody>
  </CTable>

  <CRow class="flex-lg-row flex-column-reverse">
    <CCol lg="8">
      <Pagination
        :active-page="page"
        :limit="8"
        :pages="postCases(10)"
        class="mt-3"
        @active-page-change="pageSelect"
      />
    </CCol>
    <CCol lg="4" class="text-right pt-3">
      <CButton
        color="primary"
        class="px-5"
        @click="$router.push({ name: '본사 소송사건 - 작성' })"
      >
        등록하기
      </CButton>
    </CCol>
  </CRow>
</template>
