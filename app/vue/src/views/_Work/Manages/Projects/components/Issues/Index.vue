<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { onBeforeRouteUpdate, useRoute, useRouter } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import IssueList from '@/views/_Work/Manages/Issues/components/IssueList.vue'
import IssueForm from '@/views/_Work/Manages/Issues/components/IssueForm.vue'
import IssueView from '@/views/_Work/Manages/Issues/components/IssueView.vue'

const emit = defineEmits(['aside-visible'])

const [route, router] = [useRoute(), useRouter()]

const workStore = useWork()
const iProject = computed(() => workStore.issueProject)
const issueProjects = computed(() => workStore.AllIssueProjects)
const issue = computed(() => workStore.issue)
const issueList = computed(() => workStore.issueList)
const issueLogList = computed(() => workStore.issueLogList)
const issueCommentList = computed(() => workStore.issueCommentList)
const timeEntryList = computed(() => workStore.timeEntryList)

const onSubmit = (payload: any) => {
  if (payload.pk) workStore.updateIssue(payload)
  else {
    workStore.createIssue(payload)
    router.replace({ name: '(업무)' })
  }
}

onBeforeRouteUpdate(async to => {
  if (to.params.issueId) {
    await workStore.fetchIssue(Number(to.params.issueId))
    await workStore.fetchIssueLogList({ issue: Number(to.params.issueId) })
  } else {
    workStore.issue = null
    await workStore.fetchIssueList()
  }
})

onBeforeMount(async () => {
  emit('aside-visible', true)
  await workStore.fetchIssueList()

  if (route.params.projId) await workStore.fetchIssueProject(route.params.projId as string)

  if (route.params.issueId) {
    await workStore.fetchIssueProjectList()
    await workStore.fetchIssue(Number(route.params.issueId))
    await workStore.fetchIssueLogList({ issue: Number(route.params.issueId) })
    await workStore.fetchTimeEntryList({ issue: Number(route.params.issueId) })
  }
})
</script>

<template>
  <IssueList v-if="route.name === '(업무)'" :issue-list="issueList" />

  <IssueView
    v-if="route.name === '(업무) - 보기' && issue"
    :i-project="iProject ?? undefined"
    :issue="issue"
    :issue-projects="issueProjects"
    :issue-log-list="issueLogList"
    :issue-comment-list="issueCommentList"
    :time-entry-list="timeEntryList"
    @on-submit="onSubmit"
  />

  <IssueForm
    v-if="route.name === '(업무) - 추가'"
    :issue-projects="issueProjects"
    @on-submit="onSubmit"
    @close-form="router.push({ name: '(업무)' })"
  />
</template>
