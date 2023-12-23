<script setup lang="ts">
import { type PropType } from 'vue'
import type { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

defineProps({
  post: { type: Object as PropType<Post>, default: null },
  viewRoute: { type: String, required: true },
})
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>{{ post.pk }}</CTableDataCell>
    <CTableDataCell>{{ post.board_name }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link :to="{ name: `${viewRoute} - 보기`, params: { postId: post.pk } }">
        {{ cutString(post.title, 50) }}
      </router-link>
      <CBadge v-if="post.is_new" color="warning" size="sm" class="ml-2">new</CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(post.created ?? '') }}</CTableDataCell>
    <CTableDataCell>{{ post.hit }}</CTableDataCell>
  </CTableRow>
</template>
