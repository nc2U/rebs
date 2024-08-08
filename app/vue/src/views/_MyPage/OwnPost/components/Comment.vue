<script lang="ts" setup>
import { computed, type PropType } from 'vue'
import { timeFormat } from '@/utils/baseMixins'
import type { Board, Comment as Cm } from '@/store/types/board'

const props = defineProps({
  boardList: { type: Array as PropType<Board[]>, default: () => [] },
  comment: { type: Object as PropType<Cm>, default: null },
})

const viewRoute = computed(() => {
  const board = props.boardList.filter(b => b.pk === props.comment?.post?.board)[0]

  return board && board.name ? board.name : '공지 사항'
})
</script>

<template>
  <CTableRow class="text-50 text-center" :id="`comment_${comment.pk}`">
    <CTableDataCell>{{ comment.pk }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        :to="{ name: `${viewRoute} - 보기`, params: { postId: comment.post.pk } }"
        target="_blank"
      >
        {{ comment.content }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(comment.created as string) }}</CTableDataCell>
  </CTableRow>
</template>
