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
  if (route.params.issueId) workStore.fetchIssue(Number(route.params.issueId))
})
</script>

<template>
  <IssueList v-if="route.name === '(업무)'" :issue-list="issueList" />

  <IssueView v-if="route.name === '(업무) - 보기'" :issue="issue ?? null" />
</template>
