<script lang="ts" setup>
import { type PropType } from 'vue'
import type { TimeEntry } from '@/store/types/work'

defineProps({
  timeEntryList: { type: Array as PropType<TimeEntry[]>, default: () => [] },
})
</script>

<template>
  <div>{{ timeEntryList }}</div>
</template>
