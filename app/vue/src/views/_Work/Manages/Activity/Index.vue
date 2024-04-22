<script setup lang="ts">
import { ref, computed, type ComputedRef, inject, onBeforeMount } from 'vue'
import { navMenu1, navMenu2 } from '@/views/_Work/_menu/headermixin1'
import { useWork } from '@/store/pinia/work'
import type { Company } from '@/store/types/settings'
import type { ActLogEntryFilter } from '@/store/types/work'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import ActivityLogList from '@/views/_Work/Manages/Activity/components/ActivityLogList.vue'
import AsideActivity from '@/views/_Work/Manages/Activity/components/aside/AsideActivity.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const sideNavCAll = () => cBody.value.toggle()

const navMenu = computed(() => (!issueProjects.value.length ? navMenu1 : navMenu2))

const workStore = useWork()
const issueProjects = computed(() => workStore.issueProjects)

const toDate = ref(new Date())

const toBack = (date: Date) => (toDate.value = date)
const toNext = (date: Date) => (toDate.value = date)

const filterActivity = (payload: ActLogEntryFilter) => {
  console.log(payload)
  if (payload.to_act_date) toDate.value = payload.to_act_date
  workStore.fetchActivityLogList(payload)
}

onBeforeMount(() => {
  workStore.fetchIssueProjectList({})
})
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <ActivityLogList :to-date="toDate" @to-back="toBack" @to-next="toNext" />
    </template>

    <template v-slot:aside>
      {{ toDate }}
      <AsideActivity :to-date="toDate" @filter-activity="filterActivity" />
    </template>
  </ContentBody>
</template>
