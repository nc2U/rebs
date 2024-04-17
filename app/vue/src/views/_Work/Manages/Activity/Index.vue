<script setup lang="ts">
import { computed, type ComputedRef, inject, onBeforeMount, ref, watch } from 'vue'
import { navMenu1, navMenu2 } from '@/views/_Work/_menu/headermixin1'
import { useWork } from '@/store/pinia/work'
import { dateFormat } from '@/utils/baseMixins'
import type { Company } from '@/store/types/settings'
import type { ActLogEntry } from '@/store/types/work'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import ActivityLogList from '@/views/_Work/Manages/Activity/components/ActivityLogList.vue'
import AsideActivity from '@/views/_Work/Manages/Activity/components/aside/AsideActivity.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const sideNavCAll = () => cBody.value.toggle()

const navMenu = computed(() => (!issueProjectList.value.length ? navMenu1 : navMenu2))

const workStore = useWork()
const issueProjectList = computed(() => workStore.issueProjectList)
const groupedActivities = computed<{ [key: string]: ActLogEntry[] }>(
  () => workStore.groupedActivities,
)

const fromDate = computed(() => new Date(toDate.value.getTime() - 9 * 24 * 60 * 60 * 1000))

const toDate = ref(new Date())
watch(toDate, async nVal => {
  if (nVal) {
    await workStore.fetchActivityLogList({
      from_act_date: dateFormat(fromDate.value),
      to_act_date: dateFormat(nVal),
    })
  }
})

const toBack = () => (toDate.value = new Date(toDate.value.setDate(toDate.value.getDate() - 10)))
const toNext = () => (toDate.value = new Date(toDate.value.setDate(toDate.value.getDate() + 10)))

onBeforeMount(() => {
  workStore.fetchIssueProjectList({})
  workStore.fetchActivityLogList({
    from_act_date: dateFormat(fromDate.value),
    to_act_date: dateFormat(toDate.value),
  })
})
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <ActivityLogList
        :grouped-activities="groupedActivities"
        :from-date="fromDate"
        :to-date="toDate"
        @to-back="toBack"
        @to-next="toNext"
      />
    </template>

    <template v-slot:aside>
      <AsideActivity />
    </template>
  </ContentBody>
</template>
