<script setup lang="ts">
import type { PropType } from 'vue'
import { useDocs } from '@/store/pinia/docs'
import { TableSecondary } from '@/utils/cssMixins'
import type { Docs as D } from '@/store/types/docs'
import Pagination from '@/components/Pagination'
import Docs from './Docs.vue'

defineProps({
  page: { type: Number, default: 1 },
  docsList: { type: Array as PropType<D[]>, default: () => [] },
  viewRoute: { type: String, required: true },
})

const emit = defineEmits(['page-select'])

const docStore = useDocs()

const docsPages = (num: number) => docStore.docsPages(num)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col style="width: 5%" />
      <col style="width: 20%" />
      <col style="width: 50%" />
      <col style="width: 25%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="TableSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">게시판</CTableHeaderCell>
        <CTableHeaderCell scope="col">제목</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록일시</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Docs v-for="docs in docsList" :key="docs.pk" :docs="docs" :view-route="viewRoute" />
    </CTableBody>
  </CTable>

  <CRow class="flex-lg-row flex-column-reverse">
    <CCol lg="8">
      <Pagination
        :active-page="page"
        :limit="8"
        :pages="docsPages(10)"
        class="mt-3"
        @active-page-change="pageSelect"
      />
    </CCol>
  </CRow>
</template>
