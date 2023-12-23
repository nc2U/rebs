<script setup lang="ts">
import type { PropType } from 'vue'
import { useDocument } from '@/store/pinia/document'
import { TableSecondary } from '@/utils/cssMixins'
import type { Post as P } from '@/store/types/document'
import Pagination from '@/components/Pagination'
import Post from './Post.vue'

defineProps({
  page: { type: Number, default: 1 },
  postList: { type: Array as PropType<P[]>, default: () => [] },
  viewRoute: { type: String, required: true },
})

const emit = defineEmits(['page-select'])

const documentStore = useDocument()

const postPages = (num: number) => documentStore.postPages(num)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col style="width: 10%" />
      <col style="width: 15%" />
      <col style="width: 40%" />
      <col style="width: 20%" />
      <col style="width: 15%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="TableSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">게시판</CTableHeaderCell>
        <CTableHeaderCell scope="col">제목</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록일시</CTableHeaderCell>
        <CTableHeaderCell scope="col">조회수</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Post v-for="post in postList" :key="post.pk" :post="post" :view-route="viewRoute" />
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
  </CRow>
</template>
