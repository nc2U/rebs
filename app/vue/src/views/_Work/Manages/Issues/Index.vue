<script setup lang="ts">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { navMenu2 as navMenu } from '@/views/_Work/_menu/headermixin1'
import type { Company } from '@/store/types/settings'
import { useRouter } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import IssueList from './components/IssueList.vue'
import IssueForm from '@/views/_Work/Manages/Issues/components/IssueForm.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const sideNavCAll = () => cBody.value.toggle()

const workStore = useWork()
const issueList = computed(() => workStore.issueList)
const allProjects = computed(() => workStore.AllIssueProjects)

///
const statusList = computed(() => workStore.statusList)
const activityList = computed(() => workStore.activityList)
const priorityList = computed(() => workStore.priorityList)
const getIssues = computed(() => workStore.getIssues)

const router = useRouter()

const onSubmit = (payload: any) => {
  if (payload.pk) workStore.updateIssue(payload)
  else {
    workStore.createIssue(payload)
    router.replace({ name: '업무' })
  }
}

onBeforeMount(async () => {
  await workStore.fetchAllIssueProjectList()
  await workStore.fetchIssueList({ status__closed: '' })

  ///////
  await workStore.fetchMemberList()
  await workStore.fetchTrackerList()
  await workStore.fetchStatusList()
  await workStore.fetchActivityList()
  await workStore.fetchPriorityList()
})
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <IssueList
        v-if="$route.name === '업무'"
        :issue-list="issueList"
        :all-projects="allProjects"
      />

      <IssueForm
        v-if="$route.name === '업무 - 추가'"
        :all-projects="allProjects"
        :status-list="statusList"
        :activity-list="activityList"
        :priority-list="priorityList"
        :get-issues="getIssues"
        @on-submit="onSubmit"
        @close-form="router.push({ name: '업무' })"
      />
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
