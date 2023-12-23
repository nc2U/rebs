<script setup lang="ts">
import { computed, type PropType } from 'vue'
import type { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

const props = defineProps({
  post: { type: Object as PropType<Post>, default: null },
  viewRoute: { type: String, required: true },
})

const whichBoard = computed(() => {
  if (props.post?.board === 1) return `공지 사항`
  if (!!props.post?.company)
    if (props.post.board === 2) return '본사 일반 문서'
    else if (props.post.board === 3) return '본사 소송 문서'
    else if (!!props.post?.project)
      if (props.post.board === 2) return '현장 일반 문서'
      else if (props.post.board === 3) return '현장 소송 문서'
  return '공지 사항'
})
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>{{ post.pk }}</CTableDataCell>
    <CTableDataCell>{{ post.board_name }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        :to="{ name: `${whichBoard} - 보기`, params: { postId: post.pk } }"
        target="_blank"
      >
        {{ cutString(post.title, 50) }}
      </router-link>
      <CBadge v-if="post.is_new" color="warning" size="sm" class="ml-2">new</CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(post.created ?? '') }}</CTableDataCell>
  </CTableRow>
</template>
