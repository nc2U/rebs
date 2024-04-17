<script lang="ts" setup>
import { onBeforeMount } from 'vue'
import ActivityLogList from '@/views/_Work/Manages/Activity/components/ActivityLogList.vue'

const emit = defineEmits(['aside-visible'])

onBeforeMount(() => {
  emit('aside-visible', true)
})
</script>

<template>
  <ActivityLogList />
</template>
