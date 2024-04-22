<script lang="ts" setup>
import { onBeforeMount } from 'vue'
import ActivityLogList from '@/views/_Work/Manages/Activity/components/ActivityLogList.vue'

defineProps({ toDate: { type: Date, required: true } })

const emit = defineEmits(['aside-visible'])

onBeforeMount(() => {
  emit('aside-visible', true)
})
</script>

<template>
  <ActivityLogList :to-date="toDate" />
</template>
