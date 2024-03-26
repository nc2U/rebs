<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { onBeforeRouteUpdate, useRoute, useRouter } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import IssueList from '@/views/_Work/Manages/Issues/components/IssueList.vue'
import IssueForm from '@/views/_Work/Manages/Issues/components/IssueForm.vue'
import IssueView from './components/IssueView.vue'

const emit = defineEmits(['aside-visible'])

const [route, router] = [useRoute(), useRouter()]

const workStore = useWork()
const issue = computed(() => workStore.issue)
const issueList = computed(() => workStore.issueList)
const logEntryList = computed(() => workStore.logEntryList)
const iProject = computed(() => workStore.issueProject)
const issueProjects = computed(() => workStore.AllIssueProjects)

const onSubmit = (payload: any) => {
  console.log(payload)
  if (payload.pk) alert('issue update!')
  else alert('issue create!')
  router.replace({ name: '(업무)' })
}

onBeforeRouteUpdate(async to => {
  if (to.params.issueId) {
    await workStore.fetchIssue(Number(to.params.issueId))
    await workStore.fetchLogEntryList({ issue: to.params.issueId as string })
  } else {
    workStore.issue = null
    await workStore.fetchIssueList()
  }
})

onBeforeMount(() => {
  emit('aside-visible', true)
  workStore.fetchIssueList()

  if (route.params.projId) workStore.fetchIssueProject(route.params.projId as string)

  if (route.params.issueId) {
    workStore.fetchIssueProjectList()
    workStore.fetchIssue(Number(route.params.issueId))
    workStore.fetchLogEntryList({ issue: route.params.issueId as string })
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
    :log-entry-list="logEntryList"
    @on-submit="onSubmit"
  />

  <CRow v-if="route.name === '(업무) - 추가'" class="py-2">
    <CCol>
      <h5>새 업무만들기</h5>
    </CCol>

    <IssueForm
      :i-project="iProject ?? undefined"
      :issue-projects="issueProjects"
      @on-submit="onSubmit"
      @close-form="router.push({ name: '(업무)' })"
    />
  </CRow>
</template>
