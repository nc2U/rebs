<script setup lang="ts">
import type { PropType } from 'vue'
import { useDocument } from '@/store/pinia/document'
import { TableSecondary } from '@/utils/cssMixins'
import Docs from './Docs.vue'
import Pagination from '@/components/Pagination'
import type { Post } from '@/store/types/document'

defineProps({
  project: { type: Number, default: null },
  page: { type: Number, default: 1 },
  postList: { type: Array as PropType<Post[]>, default: () => [] },
})

const emit = defineEmits(['page-select', 'sort-filter'])

const documentStore = useDocument()

const postPages = (num: number) => documentStore.postPages(num)
const pageSelect = (page: number) => emit('page-select', page)
const sortFilter = (project: number | null) => emit('sort-filter', project)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col style="width: 8%" />
      <col style="width: 10%" />
      <col style="width: 11%" />
      <col style="width: 34%" />
      <col style="width: 12%" />
      <col style="width: 15%" />
      <col style="width: 10%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="TableSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">구분</CTableHeaderCell>
        <CTableHeaderCell scope="col">문서 시행일자</CTableHeaderCell>
        <CTableHeaderCell scope="col">문서 제목</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록자</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록일시</CTableHeaderCell>
        <CTableHeaderCell scope="col">조회수</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Docs v-for="post in postList" :key="post.pk" :post="post" @sort-filter="sortFilter" />
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
        :disabled="!project"
        @click="$router.push({ name: '본사 일반 문서 - 작성' })"
      >
        등록하기
      </CButton>
    </CCol>
  </CRow>
</template>
