<script lang="ts" setup>
import { ref, computed, type PropType } from 'vue'
import { useBoard } from '@/store/pinia/board'
import { TableSecondary } from '@/utils/cssMixins'
import type { Board, Comment as Cm } from '@/store/types/board'
import Pagination from '@/components/Pagination'
import Comment from './Comment.vue'

defineProps({
  boardList: { type: Array as PropType<Board[]>, default: () => [] },
  comments: { type: Array as PropType<Cm[]>, default: () => [] },
})
const emit = defineEmits(['vision-toggle', 'to-like', 'on-submit', 'form-reset', 'page-select'])

const boardStore = useBoard()
const commentCount = computed(() => boardStore.commentCount)

const pageSelect = (page: number) => emit('page-select', page)

const itemsPerPage = ref(10)
const commentPages = (pages: number) => Math.ceil(commentCount.value / pages)
</script>

<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col style="width: 20%" />
      <col style="width: 50%" />
      <col style="width: 30%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="TableSecondary" class="text-center border-top-1">
        <CTableHeaderCell scope="col">번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">내용</CTableHeaderCell>
        <CTableHeaderCell scope="col">등록일시</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Comment v-for="cmt in comments" :key="cmt.pk" :board-list="boardList" :comment="cmt" />
    </CTableBody>
  </CTable>

  <CRow v-if="commentCount > itemsPerPage" class="flex-lg-row flex-column-reverse">
    <CCol lg="8">
      <Pagination
        :active-page="1"
        :limit="8"
        :pages="commentPages(itemsPerPage)"
        class="mt-3"
        align="end"
        @active-page-change="pageSelect"
      />
    </CCol>
  </CRow>
</template>
