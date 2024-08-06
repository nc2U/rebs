<script setup lang="ts">
import { computed, type PropType } from 'vue'
import type { Docs } from '@/store/types/docs'
import { cutString, timeFormat } from '@/utils/baseMixins'

const props = defineProps({ docs: { type: Object as PropType<Docs>, default: null } })

const viewRoute = computed(() => {
  if (props.docs?.board === 1) return '공지 사항'
  if (!!props.docs?.project) {
    if (props.docs.board === 2) return '현장 일반 문서'
    else if (props.docs.board === 3) return '현장 소송 문서'
  } else {
    if (props.docs.board === 2) return '본사 일반 문서'
    else if (props.docs.board === 3) return '본사 소송 문서'
  }
  return '공지 사항'
})
</script>

<template>
  <CTableRow v-if="docs" class="text-center">
    <CTableDataCell>{{ docs.pk }}</CTableDataCell>
    <CTableDataCell>
      {{ docs.type_name }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link
        :to="{ name: `${viewRoute} - 보기`, params: { postId: docs.pk } }"
        target="_blank"
      >
        {{ cutString(docs.title, 50) }}
      </router-link>
      <CBadge v-if="docs.is_new" color="warning" size="sm" class="ml-2">new</CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(docs.created ?? '') }}</CTableDataCell>
  </CTableRow>
</template>
