<script lang="ts" setup>
import { computed, onBeforeMount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import type { TimeEntryFilter } from '@/store/types/work'
import TimeEntryList from '@/views/_Work/Manages/SpentTime/components/TimeEntryList.vue'
import TimeEntryForm from '@/views/_Work/Manages/SpentTime/components/TimeEntryForm.vue'

const emit = defineEmits(['aside-visible'])

const workStore = useWork()
const issueProject = computed(() => workStore.issueProject)
const timeEntryList = computed(() => workStore.timeEntryList)
const allProjects = computed(() => workStore.AllIssueProjects)
const createTimeEntry = (payload: any) => workStore.createTimeEntry(payload)
const updateTimeEntry = (payload: any) => workStore.updateTimeEntry(payload)
const deleteTimeEntry = (pk: number) => workStore.deleteTimeEntry(pk)

const [route, router] = [useRoute(), useRouter()]

const onSubmit = async (payload: any) => {
  if (payload.pk) await updateTimeEntry(payload)
  else {
    await createTimeEntry(payload)
    await router.replace({ name: '(소요시간)' })
  }
}

const filterSubmit = (payload: TimeEntryFilter) => {
  console.log(payload)
  workStore.fetchTimeEntryList(payload)
}

const delSubmit = (pk: number) => deleteTimeEntry(pk)

const project = computed(() => (route.params.projId ? (route.params.projId as string) : ''))
const issue = computed(() => (route.query.issue_id ? (route.query.issue_id as string) : ''))

watch(route, async nVal => {
  if (nVal.params.projId || nVal.params.issueId)
    await workStore.fetchTimeEntryList({ project: project.value, issue: Number(issue.value) })
})

onBeforeMount(async () => {
  emit('aside-visible', true)
  await workStore.fetchAllIssueProjectList()

  await workStore.fetchTimeEntryList({ project: project.value, issue: Number(issue.value) })
})
</script>

<template>
  <TimeEntryList
    v-if="$route.name === '(소요시간)'"
    :time-entry-list="timeEntryList"
    :sub-projects="issueProject?.sub_projects"
    :all-projects="allProjects"
    @filter-submit="filterSubmit"
    @del-submit="delSubmit"
  />

  <TimeEntryForm
    v-if="$route.name === '(소요시간) - 추가'"
    :all-projects="allProjects"
    @on-submit="onSubmit"
    @close-form="$router.push({ name: '(소요시간)' })"
  />

  <TimeEntryForm
    v-if="$route.name === '(소요시간) - 편집'"
    :all-projects="allProjects"
    @on-submit="onSubmit"
    @close-form="$router.push({ name: '(소요시간)' })"
  />
</template>
