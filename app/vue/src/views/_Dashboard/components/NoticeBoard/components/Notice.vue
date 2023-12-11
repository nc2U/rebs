<script setup lang="ts">
import { type PropType } from 'vue'
import type { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

defineProps({
  post: { type: Object as PropType<Post>, default: null },
})
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>{{ post.pk }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link :to="{ name: `공지 사항 - 보기`, params: { postId: post.pk } }">
        {{ cutString(post.title, 32) }}
      </router-link>
      <CBadge v-if="post.is_new" color="warning" size="sm" class="ml-2">new</CBadge>
      <CBadge v-if="post.comments?.length" color="warning" size="sm" class="ml-1">
        +{{ post.comments.length }}
      </CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ post.user }}</CTableDataCell>
    <CTableDataCell>{{ timeFormat(post.created ?? '') }}</CTableDataCell>
    <CTableDataCell>{{ post.hit }}</CTableDataCell>
  </CTableRow>
</template>
