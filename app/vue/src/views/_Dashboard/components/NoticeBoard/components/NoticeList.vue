<script setup lang="ts">
import { type PropType, inject } from 'vue'
import { useDocument } from '@/store/pinia/document'
import { TableSecondary } from '@/utils/cssMixins'
import type { User } from '@/store/types/accounts'
import type { Post } from '@/store/types/document'
import Pagination from '@/components/Pagination'
import TopNotice from './TopNotice.vue'
import Notice from './Notice.vue'

defineProps({
  page: { type: Number, default: 1 },
  noticeList: { type: Array as PropType<Post[]>, default: () => [] },
  postList: { type: Array as PropType<Post[]>, default: () => [] },
})

const emit = defineEmits(['page-select'])

const userInfo = inject<User>('userInfo')

const docStore = useDocument()
const postPages = (num: number) => docStore.postPages(num)

const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col style="width: 8%" />
      <col style="width: 34%" />
      <col style="width: 12%" />
      <col style="width: 15%" />
      <col style="width: 10%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="TableSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">제목</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록자</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록일시</CTableHeaderCell>
        <CTableHeaderCell scope="col">조회수</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <TopNotice v-for="notice in noticeList" :key="notice.pk" :post="notice" />
      <Notice v-for="post in postList" :key="post.pk" :post="post" />
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
      <CButton color="light" class="px-5" @click="$router.push({ name: `대 시 보 드` })">
        홈으로
      </CButton>
      <CButton
        v-if="userInfo?.is_superuser"
        color="primary"
        class="px-5"
        @click="$router.push({ name: `공지 사항 - 작성` })"
      >
        등록하기
      </CButton>
    </CCol>
  </CRow>
</template>
