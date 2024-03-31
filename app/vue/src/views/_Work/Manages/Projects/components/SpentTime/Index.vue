<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import TimeEntryList from '@/views/_Work/Manages/SpentTime/components/TimeEntryList.vue'

const emit = defineEmits(['aside-visible'])

const route = useRoute()

const workStore = useWork()
const timeEntryList = computed(() => workStore.timeEntryList)

onBeforeMount(() => {
  emit('aside-visible', true)
  if (route.params.projId) workStore.fetchTimeEntryList({ project: route.params.projId as string })
})
</script>

<template>
  <TimeEntryList :time-entry-list="timeEntryList" />
</template>
