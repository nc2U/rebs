<script lang="ts" setup>
import { onBeforeMount, type PropType } from 'vue'
import ActivityLogList from '@/views/_Work/Manages/Activity/components/ActivityLogsComponent.vue'

defineProps({
  toDate: { type: Date, required: true },
  activityFilter: { type: Object as PropType<any>, default: () => null },
})

const emit = defineEmits(['aside-visible', 'to-back', 'to-next'])

const toBack = (date: Date) => emit('to-back', date)
const toNext = (date: Date) => emit('to-next', date)

onBeforeMount(() => {
  emit('aside-visible', true)
})
</script>

<template>
  <ActivityLogList
    :to-date="toDate"
    :activity-filter="activityFilter"
    @to-back="toBack"
    @to-next="toNext"
  />
</template>
