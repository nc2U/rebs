<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import TimeEntryList from '@/views/_Work/Manages/SpentTime/components/TimeEntryList.vue'
import TimeEntryForm from '@/views/_Work/Manages/SpentTime/components/TimeEntryForm.vue'

const emit = defineEmits(['aside-visible'])

const workStore = useWork()
const timeEntryList = computed(() => workStore.timeEntryList)
const issueProjects = computed(() => workStore.AllIssueProjects)
const createTimeEntry = (payload: any) => workStore.createTimeEntry(payload)
const updateTimeEntry = (payload: any) => workStore.updateTimeEntry(payload)

const [route, router] = [useRoute(), useRouter()]

const onSubmit = async (payload: any) => {
  if (payload.pk) await updateTimeEntry(payload)
  else {
    await createTimeEntry(payload)
    await router.replace({ name: '(소요시간)' })
  }
}

onBeforeMount(async () => {
  emit('aside-visible', true)
  await workStore.fetchIssueProjectList({})
  const project = route.params.projId ? (route.params.projId as string) : ''
  const issue = route.query.issue_id ? (route.query.issue_id as string) : ''
  await workStore.fetchTimeEntryList({ project, issue })
})
</script>

<template>
  <TimeEntryList v-if="$route.name === '(소요시간)'" :time-entry-list="timeEntryList" />

  <TimeEntryForm
    v-if="$route.name === '(소요시간) - 추가'"
    :issue-projects="issueProjects"
    @on-submit="onSubmit"
    @close-form="$router.push({ name: '(소요시간)' })"
  />

  <TimeEntryForm
    v-if="$route.name === '(소요시간) - 편집'"
    :issue-projects="issueProjects"
    @on-submit="onSubmit"
    @close-form="$router.push({ name: '(소요시간)' })"
  />
</template>
