<script setup lang="ts">
import type { PropType } from 'vue'
import { useDocs } from '@/store/pinia/docs'
import { numFormat } from '@/utils/baseMixins'
import { TableSecondary } from '@/utils/cssMixins'
import type { TrashDocs as TP } from '@/store/types/docs'
import TrashDocs from './TrashDocs.vue'
import Pagination from '@/components/Pagination'

defineProps({
  trashDocsList: { type: Array as PropType<TP[]>, default: () => [] },
  trashDocsCount: { type: Number, default: 0 },
  viewRoute: { type: String, required: true },
  page: { type: Number, default: 1 },
})

const emit = defineEmits(['page-select', 'restore-docs', 'delete-docs'])

const docStore = useDocs()
const trashDocsPages = (pages: number) => docStore.trashDocsPages(pages)
const pageSelect = (page: number) => emit('page-select', page)

const restoreDocs = (pk: number) => emit('restore-docs', pk)
const deleteDocs = (pk: number) => emit('delete-docs', pk)
</script>

<template>
  <h5 v-if="trashDocsCount">삭제 게시물 : 총 {{ numFormat(trashDocsCount) }}건</h5>

  <v-divider v-if="trashDocsCount" />

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
        <CTableHeaderCell scope="col">삭제일시</CTableHeaderCell>
        <CTableHeaderCell scope="col">삭제복원</CTableHeaderCell>
        <CTableHeaderCell scope="col">완적삭제</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <TrashDocs
        v-for="docs in trashDocsList"
        :key="docs.pk"
        :trash-docs="docs"
        :view-route="viewRoute"
        @restore-docs="restoreDocs"
        @delete-docs="deleteDocs"
      />
    </CTableBody>
  </CTable>

  <CRow class="flex-lg-row flex-column-reverse">
    <CCol lg="8">
      <Pagination
        :active-page="page"
        :limit="8"
        :pages="trashDocsPages(10)"
        class="mt-3"
        @active-page-change="pageSelect"
      />
    </CCol>
  </CRow>
</template>
