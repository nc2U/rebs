<script setup lang="ts">
import { useDocument } from '@/store/pinia/document'
import Docs from './Docs.vue'
import Pagination from '@/components/Pagination'

defineProps({
  page: { type: Number, default: 1 },
  postList: { type: Array, default: () => [] },
})

const emit = defineEmits(['sort-filter', 'page-select'])

const documentStore = useDocument()

const sortFilter = (project: number | null) => emit('sort-filter', project)

const postPages = (num: number) => documentStore.postPages(num)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="8%" />
      <col width="10%" />
      <col width="20%" />
      <col width="25%" />
      <col width="12%" />
      <col width="15%" />
      <col width="10%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="headerSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">구분</CTableHeaderCell>
        <CTableHeaderCell scope="col">사건 번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">문서 제목</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록자</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록일시</CTableHeaderCell>
        <CTableHeaderCell scope="col">조회수</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Docs
        v-for="post in postList"
        :key="post.pk"
        :post="post"
        @sort-filter="sortFilter"
      />
    </CTableBody>
  </CTable>

  <CRow class="flex-lg-row flex-column-reverse">
    <CCol lg="8">
      <Pagination
        :active-page="page"
        :limit="8"
        :pages="postPages(10)"
        class="mt-3"
        @active-page-change="pageSelect"
      />
    </CCol>
    <CCol lg="4" class="text-right pt-3">
      <CButton
        color="primary"
        class="px-5"
        @click="$router.push({ name: '본사 소송문서 - 작성' })"
      >
        등록하기
      </CButton>
    </CCol>
  </CRow>
</template>
