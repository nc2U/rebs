<script lang="ts" setup>
import { onBeforeMount } from 'vue'
import ActivityLogList from '@/views/_Work/Manages/Activity/components/ActivityLogList.vue'

defineProps({ toDate: { type: Date, required: true } })

const emit = defineEmits(['aside-visible', 'to-back', 'to-next'])

const toBack = (date: Date) => emit('to-back', date)
const toNext = (date: Date) => emit('to-next', date)

onBeforeMount(() => {
  emit('aside-visible', true)
})
</script>

<template>
  <ActivityLogList :to-date="toDate" @to-back="toBack" @to-next="toNext" />
</template>
