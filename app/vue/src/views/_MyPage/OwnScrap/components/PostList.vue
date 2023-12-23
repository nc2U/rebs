<script setup lang="ts">
import type { PropType } from 'vue'
import { useDocument } from '@/store/pinia/document'
import { TableSecondary } from '@/utils/cssMixins'
import type { Post as P } from '@/store/types/document'
import Pagination from '@/components/Pagination'
import Post from './Post.vue'

defineProps({
  company: { type: Number, default: null },
  project: { type: Number, default: null },
  page: { type: Number, default: 1 },
  postList: { type: Array as PropType<P[]>, default: () => [] },
  viewRoute: { type: String, required: true },
  isLawsuit: { type: Boolean, default: false },
  writeAuth: { type: Boolean, default: true },
})

const emit = defineEmits(['page-select'])

const documentStore = useDocument()

const postPages = (num: number) => documentStore.postPages(num)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <h5>스크랩 : 총 20건</h5>

  <v-divider />

  <CTable hover responsive align="middle">
    <colgroup>
      <col style="width: 5%" />
      <col style="width: 20%" />
      <col style="width: 35%" />
      <col style="width: 20%" />
      <col style="width: 10%" />
      <col style="width: 10%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="TableSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">게시판</CTableHeaderCell>
        <CTableHeaderCell scope="col">제목</CTableHeaderCell>
        <CTableHeaderCell scope="col">보관일시</CTableHeaderCell>
        <CTableHeaderCell scope="col">제목수정</CTableHeaderCell>
        <CTableHeaderCell scope="col">보관취소</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Post
        v-for="post in postList"
        :key="post.pk"
        :post="post"
        :view-route="viewRoute"
        :is-lawsuit="isLawsuit"
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
  </CRow>
</template>
