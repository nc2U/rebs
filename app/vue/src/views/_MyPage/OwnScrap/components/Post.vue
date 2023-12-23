<script setup lang="ts">
import { computed, type PropType } from 'vue'
import type { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

const props = defineProps({
  post: { type: Object as PropType<Post>, default: null },
})

const viewRoute = computed(() => {
  if (props.post?.board === 1) return '공지 사항'
  if (!!props.post?.project) {
    if (props.post.board === 2) return '현장 일반 문서'
    else if (props.post.board === 3) return '현장 소송 문서'
  } else {
    if (props.post.board === 2) return '본사 일반 문서'
    else if (props.post.board === 3) return '본사 소송 문서'
  }
  return '공지 사항'
})
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>{{ post.pk }}</CTableDataCell>
    <CTableDataCell>
      <router-link :to="{ name: viewRoute }">{{ post.board_name }}</router-link>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link :to="{ name: `${viewRoute} - 보기`, params: { postId: post.pk } }">
        {{ cutString(post.title, 50) }}
      </router-link>
      <CBadge v-if="post.is_new" color="warning" size="sm" class="ml-2">new</CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(post.created ?? '') }}</CTableDataCell>
    <CTableDataCell>
      <v-btn density="compact" icon="mdi-plus" rounded="1" size="sm" color="success" />
    </CTableDataCell>
    <CTableDataCell>
      <v-btn density="compact" icon="mdi-trash-can-outline" size="sm" rounded="1" color="red" />
    </CTableDataCell>
  </CTableRow>
</template>
