<script lang="ts" setup>
import { type PropType } from 'vue'
import { timeFormat } from '@/utils/baseMixins'
import type { Comment as Cm } from '@/store/types/document'

defineProps({ comment: { type: Object as PropType<Cm>, default: null } })
</script>

<template>
  <CTableRow class="text-50 text-center" :id="`comment_${comment.pk}`">
    <CTableDataCell>{{ comment.pk }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <router-link to="#" target="_blank">
        {{ comment.content }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>{{ timeFormat(comment.created as string) }}</CTableDataCell>
  </CTableRow>
</template>
