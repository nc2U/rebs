<script lang="ts" setup>
import { type PropType } from 'vue'
import type { ActLogEntry } from '@/store/types/work'

defineProps({
  groupedActivities: {
    type: Object as any,
    default: () => {},
  },
})
</script>

<template>
  <CRow class="mb-3">
    <CCol>{{ groupedActivities }}</CCol>
  </CRow>
</template>
