<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import IssueList from './components/IssueList.vue'
import IssueView from './components/IssueView.vue'

const emit = defineEmits(['aside-visible'])

const route = useRoute()

const workStore = useWork()
const issue = computed(() => workStore.issue)
const issueList = computed(() => workStore.issueList)
const logEntryList = computed(() => workStore.logEntryList)

onBeforeRouteUpdate(async to => {
  if (to.params.issueId) await workStore.fetchIssue(Number(to.params.issueId))
  else {
    workStore.issue = null
    await workStore.fetchIssueList()
  }
})

onBeforeMount(() => {
  emit('aside-visible', true)
  workStore.fetchIssueList()

  if (route.params.issueId) {
    workStore.fetchIssue(Number(route.params.issueId))
    workStore.fetchLogEntryList({ issue: route.params.issueId as string })
  }
})
</script>

<template>
  <IssueList v-if="route.name === '(업무)'" :issue-list="issueList" />

  <IssueView
    v-if="route.name === '(업무) - 보기'"
    :issue="issue ?? undefined"
    :log-entry-list="logEntryList"
  />
</template>
