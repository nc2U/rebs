<script setup lang="ts">
import { computed, PropType } from 'vue'
import { Post } from '@/store/types/document'
import { cutString, timeFormat } from '@/utils/baseMixins'

const props = defineProps({
  post: { type: Object as PropType<Post>, default: null },
})

const emit = defineEmits(['sort-filter'])

const sortName = computed(() => props.post.proj_name || '본사')
const sortColor = computed(() => (props.post.project ? 'success' : 'info'))
const lawsuitName = computed(() =>
  props.post.lawsuit_name
    ? props.post.lawsuit_name
        .replace('지방법원', '지법')
        .replace('고등법원', '고법')
        .replace('대법원', '대법')
    : '',
)

const sortFunc = () => emit('sort-filter', props.post.project)
</script>

<template>
  <CTableRow v-if="post" class="text-center">
    <CTableDataCell>{{ post.pk }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <a href="javascript:void(0);" @click="sortFunc">
        <CBadge :color="sortColor" shape="rounded-pill">{{ sortName }}</CBadge>
      </a>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(lawsuitName, 23) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        :to="{ name: '본사 소송 문서 - 보기', params: { postId: post.pk } }"
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
