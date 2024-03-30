<script setup lang="ts">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { navMenu2 as navMenu } from '@/views/_Work/_menu/headermixin1'
import { useWork } from '@/store/pinia/work'
import type { Company } from '@/store/types/settings'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import NoData from '@/views/_Work/components/NoData.vue'
import SearchList from '@/views/_Work/components/SearchList.vue'
import TimeEntryList from '@/views/_Work/Manages/SpentTime/components/TimeEntryList.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const sideNavCAll = () => cBody.value.toggle()

const workStore = useWork()
const timeEntryList = computed(() => workStore.timeEntryList)

onBeforeMount(() => {
  workStore.fetchTimeEntryList()
})
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <CRow class="py-2">
        <CCol>
          <h5>{{ $route.name }}</h5>
        </CCol>

        <CCol class="text-right">
          <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2 form-text">
            <v-icon icon="mdi-plus-circle" color="success" size="sm" />
            <router-link to="" class="ml-1">작업시간 기록</router-link>
          </span>
        </CCol>
      </CRow>

      <SearchList />

      <NoData v-if="!timeEntryList.length" />

      <CRow v-else>
        <CCol>
          <TimeEntryList :time-entry-list="timeEntryList" />
        </CCol>
      </CRow>
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
