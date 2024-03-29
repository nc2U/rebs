<script lang="ts" setup>
import { ref, computed, type PropType } from 'vue'
import { useDocument } from '@/store/pinia/document'
import type { Comment as Cm } from '@/store/types/document'
import Comment from './Comment.vue'
import Pagination from '@/components/Pagination'
import { TableSecondary } from '@/utils/cssMixins'

defineProps({ comments: { type: Array as PropType<Cm[]>, default: () => [] } })
const emit = defineEmits(['vision-toggle', 'to-like', 'on-submit', 'form-reset', 'page-select'])

const docStore = useDocument()
const commentCount = computed(() => docStore.commentCount)

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
      <Comment v-for="cmt in comments" :key="cmt.pk" :comment="cmt" />
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
