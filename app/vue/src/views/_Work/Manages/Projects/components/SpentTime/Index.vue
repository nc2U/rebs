<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import SearchList from '@/views/_Work/components/SearchList.vue'
import NoData from '@/views/_Work/components/NoData.vue'
import HeaderTab from '@/views/_Work/Manages/SpentTime/components/HeaderTab.vue'
import TimeEntryList from '@/views/_Work/Manages/SpentTime/components/TimeEntryList.vue'

const emit = defineEmits(['aside-visible'])

const route = useRoute()

const workStore = useWork()
const timeEntryList = computed(() => workStore.timeEntryList)

onBeforeMount(() => {
  emit('aside-visible', true)
  if (route.params.projId) workStore.fetchTimeEntryList({ project: route.params.projId as string })
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>소요시간</h5>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2 form-text">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link to="" class="ml-1">작업시간 기록</router-link>
      </span>
    </CCol>
  </CRow>

  <SearchList />

  <HeaderTab />

  <NoData v-if="!timeEntryList.length" />

  <CRow v-else>
    <CCol>
      <TimeEntryList :time-entry-list="timeEntryList" />
    </CCol>
  </CRow>
</template>
