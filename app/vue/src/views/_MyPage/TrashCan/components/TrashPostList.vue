<script setup lang="ts">
import type { PropType } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import { TableSecondary } from '@/utils/cssMixins'
import type { TrashPost as TP } from '@/store/types/document'
import TrashPost from './TrashPost.vue'
import Pagination from '@/components/Pagination'
import { useDocument } from '@/store/pinia/document'

defineProps({
  trashPostList: { type: Array as PropType<TP[]>, default: () => [] },
  trashPostCount: { type: Number, default: 0 },
  viewRoute: { type: String, required: true },
  page: { type: Number, default: 1 },
})

const emit = defineEmits(['page-select', 'restore-post'])

const docStore = useDocument()
const trashPostPages = (pages: number) => docStore.trashPostPages(pages)
const pageSelect = (page: number) => emit('page-select', page)

const restorePost1 = (pk: number) => emit('restore-post', pk)
</script>

<template>
  <h5>스크랩 : 총 {{ numFormat(trashPostCount) }}건</h5>

  <v-divider />

  <CTable hover responsive align="middle">
    <colgroup>
      <col style="width: 5%" />
      <col style="width: 20%" />
      <col style="width: 35%" />
      <col style="width: 20%" />
      <col style="width: 20%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="TableSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">게시판</CTableHeaderCell>
        <CTableHeaderCell scope="col">제목</CTableHeaderCell>
        <CTableHeaderCell scope="col">삭제일시</CTableHeaderCell>
        <CTableHeaderCell scope="col">삭제복원</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <TrashPost
        v-for="post in trashPostList"
        :key="post.pk"
        :trash-post="post"
        :view-route="viewRoute"
        @restore-post="restorePost1"
      />
    </CTableBody>
  </CTable>

  <CRow class="flex-lg-row flex-column-reverse">
    <CCol lg="8">
      <Pagination
        :active-page="page"
        :limit="8"
        :pages="trashPostPages(10)"
        class="mt-3"
        @active-page-change="pageSelect"
      />
    </CCol>
  </CRow>
</template>
