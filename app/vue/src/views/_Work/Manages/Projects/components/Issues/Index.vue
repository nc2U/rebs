<script lang="ts" setup>
import { computed, onBeforeMount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import type { IssueFilter } from '@/store/types/work'
import IssueList from '@/views/_Work/Manages/Issues/components/IssueList.vue'
import IssueForm from '@/views/_Work/Manages/Issues/components/IssueForm.vue'
import IssueView from '@/views/_Work/Manages/Issues/components/IssueView.vue'

const emit = defineEmits(['aside-visible'])

const [route, router] = [useRoute(), useRouter()]

const workStore = useWork()
const issueProject = computed(() => workStore.issueProject)
const allProjects = computed(() => workStore.AllIssueProjects)
const issue = computed(() => workStore.issue)
const issueList = computed(() => workStore.issueList)
const issueCommentList = computed(() => workStore.issueCommentList)
const timeEntryList = computed(() => workStore.timeEntryList)

const statusList = computed(() => workStore.statusList)
const trackerList = computed(() => workStore.trackerList)
const activityList = computed(() => workStore.activityList)
const priorityList = computed(() => workStore.priorityList)
const getIssues = computed(() => workStore.getIssues)

const onSubmit = (payload: any) => {
  if (payload.pk) workStore.updateIssue(payload)
  else {
    workStore.createIssue(payload)
    router.replace({ name: '(업무)' })
  }
}

const filterSubmit = (payload: IssueFilter) => {
  console.log(payload)
  workStore.fetchIssueList(payload)
}

watch(route, async nVal => {
  const project = nVal.params.projId as string
  await workStore.fetchIssueList({ status__closed: '0', project })
  if (nVal.params.issueId) {
    await workStore.fetchIssue(Number(nVal.params.issueId))
    await workStore.fetchIssueLogList({ issue: Number(nVal.params.issueId) })
  } else workStore.issue = null
})

onBeforeMount(async () => {
  emit('aside-visible', true)
  await workStore.fetchAllIssueProjectList()

  if (route.params.projId) {
    await workStore.fetchIssueProject(route.params.projId as string)
    const project = route.params.projId as string
    await workStore.fetchIssueList({ status__closed: '0', project })
  }

  if (route.params.issueId) {
    await workStore.fetchIssue(Number(route.params.issueId))
    await workStore.fetchIssueCommentList({ issue: Number(route.params.issueId) })
    await workStore.fetchTimeEntryList({ ordering: 'pk', issue: Number(route.params.issueId) })
  }

  await workStore.fetchMemberList()
  await workStore.fetchTrackerList()
  await workStore.fetchStatusList()
  await workStore.fetchActivityList()
  await workStore.fetchPriorityList()
})
</script>

<template>
  <IssueList
    v-if="route.name === '(업무)'"
    :issue-list="issueList"
    :all-projects="allProjects"
    :status-list="statusList"
    :tracker-list="trackerList"
    @filter-submit="filterSubmit"
  />

  <IssueView
    v-if="route.name === '(업무) - 보기' && issue"
    :issue-project="issueProject ?? undefined"
    :issue="issue"
    :all-projects="allProjects"
    :status-list="statusList"
    :activity-list="activityList"
    :priority-list="priorityList"
    :get-issues="getIssues"
    :issue-comment-list="issueCommentList"
    :time-entry-list="timeEntryList"
    @on-submit="onSubmit"
  />

  <IssueForm
    v-if="route.name === '(업무) - 추가'"
    :all-projects="allProjects"
    :status-list="statusList"
    :activity-list="activityList"
    :priority-list="priorityList"
    :get-issues="getIssues"
    @on-submit="onSubmit"
    @close-form="router.push({ name: '(업무)' })"
  />
</template>
