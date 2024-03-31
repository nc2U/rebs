<script setup lang="ts">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { navMenu2 as navMenu } from '@/views/_Work/_menu/headermixin1'
import { useWork } from '@/store/pinia/work'
import type { Company } from '@/store/types/settings'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import TimeEntryList from '@/views/_Work/Manages/SpentTime/components/TimeEntryList.vue'
import TimeEntryForm from '@/views/_Work/Manages/SpentTime/components/TimeEntryForm.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const sideNavCAll = () => cBody.value.toggle()

const workStore = useWork()
const timeEntry = computed(() => workStore.timeEntry)
const timeEntryList = computed(() => workStore.timeEntryList)

onBeforeMount(() => {
  workStore.fetchTimeEntryList({})
})
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <TimeEntryList v-if="$route.name === '소요시간'" :time-entry-list="timeEntryList" />

      <CRow v-if="$route.name === '소요시간 - 추가'" class="py-2">
        <CCol>
          <h5>소요시간</h5>
        </CCol>

        <TimeEntryForm :time-entry="timeEntry" />
      </CRow>
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
