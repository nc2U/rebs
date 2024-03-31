<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import TimeEntryList from '@/views/_Work/Manages/SpentTime/components/TimeEntryList.vue'
import TimeEntryForm from '@/views/_Work/Manages/SpentTime/components/TimeEntryForm.vue'

const emit = defineEmits(['aside-visible'])

const route = useRoute()

const workStore = useWork()
const timeEntry = computed(() => workStore.timeEntry)
const timeEntryList = computed(() => workStore.timeEntryList)
const issueProjects = computed(() => workStore.AllIssueProjects)

const onSubmit = (payload: any) => payload

onBeforeMount(async () => {
  emit('aside-visible', true)
  await workStore.fetchIssueProjectList()
  if (route.params.projId)
    await workStore.fetchTimeEntryList({ project: route.params.projId as string })
  if (route.params.timeId) await workStore.fetchTimeEntry(route.params.timeId)
  else workStore.timeEntry = null
})
</script>

<template>
  <TimeEntryList v-if="$route.name === '(소요시간)'" :time-entry-list="timeEntryList" />

  <TimeEntryForm
    v-if="$route.name.includes('(소요시간) -')"
    :time-entry="timeEntry"
    :issue-projects="issueProjects"
    @on-submit="onSubmit"
    @close-form="$router.push({ name: '(소요시간)' })"
  />
</template>
