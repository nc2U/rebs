<script setup lang="ts">
import { computed, type PropType } from 'vue'
import type { Board, Post } from '@/store/types/board'
import { cutString, timeFormat } from '@/utils/baseMixins'

const props = defineProps({
  boardList: { type: Array as PropType<Board[]>, default: () => [] },
  post: { type: Object as PropType<Post>, default: null },
})

const viewRoute = computed(() => {
  const board = props.boardList.filter(b => b.pk === props.post?.board)[0]

  return board && board.name ? board.name : '공지 사항'
})
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>{{ post.pk }}</CTableDataCell>
    <CTableDataCell>
      <router-link :to="{ name: viewRoute }" target="_blank">{{ post.board_name }}</router-link>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        :to="{ name: `${viewRoute} - 보기`, params: { postId: post.pk } }"
        target="_blank"
      >
        {{ cutString(post.title, 50) }}
      </router-link>
      <CBadge v-if="post.is_new" color="warning" size="sm" class="ml-2">new</CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(post.created ?? '') }}</CTableDataCell>
  </CTableRow>
</template>
