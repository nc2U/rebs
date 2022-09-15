<script setup lang="ts">
import { PropType } from 'vue'
import { Post } from '@/store/types/document'
import { timeFormat } from '@/utils/baseMixins'

defineProps({ post: { type: Object as PropType<Post>, default: null } })
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>{{ post.pk }}</CTableDataCell>
    <CTableDataCell>{{ post.project }}</CTableDataCell>
    <CTableDataCell>{{ post.execution_date }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ post.title }}</CTableDataCell>
    <CTableDataCell>{{ post.user }}</CTableDataCell>
    <CTableDataCell>{{ timeFormat(post.created) }}</CTableDataCell>
    <CTableDataCell>{{ post.hit }}</CTableDataCell>
  </CTableRow>
</template>
