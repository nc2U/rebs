<script setup lang="ts">
import { ref } from 'vue'

defineProps({ post: { type: Object, default: null } })

const msg = ref('Docs')
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>{{ post.pk }}</CTableDataCell>
    <CTableDataCell>{{ post.project }}</CTableDataCell>
    <CTableDataCell>{{ post.execution_date }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ post.title }}</CTableDataCell>
    <CTableDataCell>{{ '---' }}</CTableDataCell>
    <CTableDataCell>{{ '---' }}</CTableDataCell>
    <CTableDataCell>{{ post.hit }}</CTableDataCell>
  </CTableRow>
</template>
