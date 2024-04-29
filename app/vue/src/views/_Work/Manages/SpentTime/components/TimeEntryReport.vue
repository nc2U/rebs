<script lang="ts" setup>
import { type PropType } from 'vue'
import type { IssueProject, TimeEntryFilter } from '@/store/types/work'
import SearchList from './SearchList.vue'
import HeaderTab from '@/views/_Work/Manages/SpentTime/components/HeaderTab.vue'

defineProps({
  subProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
  allProjects: { type: Array as PropType<IssueProject[]>, default: () => [] },
  getIssues: { type: Array as PropType<{ value: number; label: string }[]>, default: () => [] },
  getMembers: { type: Array as PropType<{ value: number; label: string }[]>, default: () => [] },
})

const emit = defineEmits(['filter-submit'])

const filterSubmit = (payload: TimeEntryFilter) => emit('filter-submit', payload)
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>소요시간</h5>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2 form-text">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link
          :to="{ name: $route.params.projId ? '(소요시간) - 추가' : '소요시간 - 추가' }"
          class="ml-1"
        >
          작업시간 기록
        </router-link>
      </span>
    </CCol>
  </CRow>

  <SearchList
    :sub-projects="subProjects"
    :all-projects="allProjects"
    :getIssues="getIssues"
    :get-members="getMembers"
    @filter-submit="filterSubmit"
  />

  <HeaderTab />
</template>
