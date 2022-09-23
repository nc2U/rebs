<script setup lang="ts">
import { computed, PropType } from 'vue'
import { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

const props = defineProps({
  post: { type: Object as PropType<Post>, default: null },
})

const sortName = computed(() => props.post.proj_name || '본사')
const sortColor = computed(() => (props.post.project ? 'success' : 'info'))
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>{{ post.pk }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <CBadge :color="sortColor">{{ sortName }}</CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ post.execution_date }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        :to="{ name: '본사 일반문서 - 보기', params: { postId: post.pk } }"
      >
        {{ cutString(post.title, 30) }}
      </router-link>
      <CBadge v-if="post.is_new" color="warning" size="sm" class="ml-2">
        new
      </CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ post.user }}</CTableDataCell>
    <CTableDataCell>{{ timeFormat(post.created) }}</CTableDataCell>
    <CTableDataCell>{{ post.hit }}</CTableDataCell>
  </CTableRow>
</template>
