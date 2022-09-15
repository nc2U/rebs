<script setup lang="ts">
import { computed, onBeforeMount, ref, watch } from 'vue'
import { useDocument, PostFilter } from '@/store/pinia/document'
import Docs from './Docs.vue'
import Pagination from '@/components/Pagination'

const props = defineProps({ tabValue: { type: Number, default: 0 } })
const emit = defineEmits(['page-select'])

const tab = ref(0)

const documentStore = useDocument()
const postList = computed(() => documentStore.postList)

const fetchPostList = (payload: PostFilter) =>
  documentStore.fetchPostList(payload)

watch(props, val => {
  tab.value = val.tabValue
  fetchPostList({ board: 1, category: tab.value })
})

onBeforeMount(() => fetchPostList({ board: 1 }))

const postPages = (num: number) => documentStore.postPages(num)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="6%" />
      <col width="15%" />
      <col width="12%" />
      <col width="30%" />
      <col width="12%" />
      <col width="17%" />
      <col width="8%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="headerSecondary" class="text-center border-top-1">
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
      <Docs v-for="post in postList" :key="post.pk" :post="post" />
    </CTableBody>
  </CTable>

  <CRow>
    <CCol md="10">
      <Pagination
        :active-page="1"
        :limit="8"
        :pages="postPages(10)"
        class="mt-3"
        @active-page-change="pageSelect"
      />
    </CCol>
    <CCol>
      <div class="justify-content-md-end">
        <CCol>
          <CButton color="primary">등록하기</CButton>
        </CCol>
      </div>
    </CCol>
  </CRow>
</template>
