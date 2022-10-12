<script setup lang="ts">
import { useDocument } from '@/store/pinia/document'
import Case from './Case.vue'
import Pagination from '@/components/Pagination'

defineProps({
  page: { type: Number, default: 1 },
  caseList: { type: Array, default: () => [] },
})

const emit = defineEmits([
  'page-select',
  'agency-filter',
  'agency-search',
  'related-filter',
])

const documentStore = useDocument()

const agencyFilter = (court: string) => emit('agency-filter', court)
const agencySearch = (agent: string) => emit('agency-search', agent)
const relatedFilter = (related: number) => emit('related-filter', related)

const casePages = (num: number) => documentStore.casePages(num)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive align="middle" class="mt-5">
    <colgroup>
      <col width="8%" />
      <col width="8%" />
      <col width="12%" />
      <col width="10%" />
      <col width="20%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="headerSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">구분</CTableHeaderCell>
        <CTableHeaderCell scope="col">심급</CTableHeaderCell>
        <CTableHeaderCell scope="col">관할법원 / 처리기관</CTableHeaderCell>
        <CTableHeaderCell scope="col">관련사건</CTableHeaderCell>
        <CTableHeaderCell scope="col">사건명</CTableHeaderCell>
        <CTableHeaderCell scope="col">원고 / 신청인</CTableHeaderCell>
        <CTableHeaderCell scope="col">피고 / 피신청인</CTableHeaderCell>
        <CTableHeaderCell scope="col">제3채무자</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Case
        v-for="suitcase in caseList"
        :key="suitcase.pk"
        :suit-case="suitcase"
        @agency-filter="agencyFilter"
        @agency-search="agencySearch"
        @related-filter="relatedFilter"
      />
    </CTableBody>
  </CTable>

  <CRow class="flex-lg-row flex-column-reverse">
    <CCol lg="8">
      <Pagination
        :active-page="page"
        :limit="8"
        :pages="casePages(10)"
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
