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
  <CTable hover responsive align="middle">
    <colgroup v-if="isLawsuit">
      <col style="width: 8%" />
      <col style="width: 10%" />
      <col style="width: 9%" />
      <col style="width: 20%" />
      <col style="width: 27%" />
      <col style="width: 9%" />
      <col style="width: 12%" />
      <col style="width: 8%" />
    </colgroup>
    <colgroup v-else>
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
        <CTableHeaderCell scope="col">문서 발행일자</CTableHeaderCell>
        <CTableHeaderCell v-if="isLawsuit" scope="col">사건명</CTableHeaderCell>
        <CTableHeaderCell scope="col">문서 제목</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록자</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록일시</CTableHeaderCell>
        <CTableHeaderCell scope="col">조회수</CTableHeaderCell>
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
    <CCol lg="4" class="text-right pt-3">
      <CButton
        v-if="writeAuth"
        color="primary"
        class="px-5"
        :disabled="!company && !project"
        @click="$router.push({ name: `${viewRoute} - 작성` })"
      >
        등록하기
      </CButton>
    </CCol>
  </CRow>
</template>
