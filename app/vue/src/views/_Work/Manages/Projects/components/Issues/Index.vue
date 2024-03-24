<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import IssueList from './components/IssueList.vue'
import IssueView from './components/IssueView.vue'
import IssueForm from '@/views/_Work/Manages/Issues/components/IssueForm.vue'

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
    v-if="route.name === '(업무) - 보기' && issue"
    :issue="issue"
    :log-entry-list="logEntryList"
  />

  <CRow v-if="route.name === '(업무) - 추가'" class="py-2">
    <CCol>
      <h5>
        <span>{{ issue?.tracker }} #{{ issue?.pk }}</span>
        <CBadge color="primary" variant="outline" class="ml-2">진행중</CBadge>
      </h5>
    </CCol>

    <IssueForm />
  </CRow>
</template>
