<script lang="ts" setup>
import { computed, type PropType } from 'vue'
import { timeFormat } from '@/utils/baseMixins'
import type { Comment as Cm } from '@/store/types/document'

const props = defineProps({ comment: { type: Object as PropType<Cm>, default: null } })

const whichBoard = computed(() => {
  if (props.comment.post.board === 1) return `공지 사항 - 보기`
  if (!!props.comment.post.company)
    if (props.comment.post.board === 2) return '본사 일반 문서 - 보기'
    else if (props.comment.post.board === 3) return '본사 소송 문서 - 보기'
    else if (!!props.comment.post.project)
      if (props.comment.post.board === 2) return '현장 일반 문서 - 보기'
      else if (props.comment.post.board === 3) return '현장 소송 문서 - 보기'
  return '공지 사항 - 보기'
})
</script>

<template>
  <CTableRow class="text-50 text-center" :id="`comment_${comment.pk}`">
    <CTableDataCell>{{ comment.pk }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link :to="{ name: whichBoard, params: { postId: comment.post.pk } }" target="_blank">
        {{ comment.content }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(comment.created as string) }}</CTableDataCell>
  </CTableRow>
</template>
