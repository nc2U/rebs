<script setup lang="ts">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { navMenu2 as navMenu } from '@/views/_Work/_menu/headermixin1'
import { useWork } from '@/store/pinia/work'
import { useRouter } from 'vue-router'
import { useAccount } from '@/store/pinia/account'
import type { Company } from '@/store/types/settings'
import type { TimeEntryFilter } from '@/store/types/work'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import TimeEntryList from '@/views/_Work/Manages/SpentTime/components/TimeEntryList.vue'
import TimeEntryForm from '@/views/_Work/Manages/SpentTime/components/TimeEntryForm.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const sideNavCAll = () => cBody.value.toggle()

const workStore = useWork()
const allProjects = computed(() => workStore.AllIssueProjects)
const timeEntryList = computed(() => workStore.timeEntryList)
const getIssues = computed(() => workStore.getIssues)
const getMembers = computed(() => accStore.getUsers)

const createTimeEntry = (payload: any) => workStore.createTimeEntry(payload)
const updateTimeEntry = (payload: any) => workStore.updateTimeEntry(payload)

const router = useRouter()
const onSubmit = async (payload: any) => {
  if (payload.pk) await updateTimeEntry(payload)
  else {
    await createTimeEntry(payload)
    await router.replace({ name: '소요시간' })
  }
  console.log(payload)
}

const filterSubmit = (payload: TimeEntryFilter) => {
  console.log(payload)
  workStore.fetchTimeEntryList(payload)
}

const pageSelect = (page: number) => workStore.fetchTimeEntryList({ page })

const delSubmit = (pk: number) => alert(pk)

const accStore = useAccount()
onBeforeMount(() => {
  workStore.fetchAllIssueProjectList()
  workStore.fetchTimeEntryList({})
  workStore.fetchIssueList({ status__closed: '0' })
  accStore.fetchUsersList()
})
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <TimeEntryList
        v-if="$route.name === '소요시간'"
        :time-entry-list="timeEntryList"
        :all-projects="allProjects"
        :get-issues="getIssues"
        :get-members="getMembers"
        @filter-submit="filterSubmit"
        @page-select="pageSelect"
        @del-submit="delSubmit"
      />

      <TimeEntryForm
        v-if="$route.name === '소요시간 - 추가'"
        :all-projects="allProjects"
        @on-submit="onSubmit"
        @close-form="$router.push({ name: '소요시간' })"
      />
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
