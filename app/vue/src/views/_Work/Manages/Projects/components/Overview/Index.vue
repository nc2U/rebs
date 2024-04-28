<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useWork } from '@/store/pinia/work'
import type { SimpleMember } from '@/store/types/work'
import OverViewHeader from './components/OverViewHeader.vue'
import TimeSummary from './components/TimeSummary.vue'
import IssueTracker from './components/IssueTracker.vue'
import MemberBox from './components/MemberBox.vue'
import SubProjects from './components/SubProjects.vue'

const emit = defineEmits(['aside-visible'])

const workStore = useWork()
const iProject = computed(() => workStore.issueProject)

const allMembers = computed<SimpleMember[]>(() => workStore.issueProject?.all_members ?? [])

const computedMembers = computed(() => {
  const organizedData = {} as { [key: string]: Array<{ pk: number; username: string }> }

  allMembers.value.forEach(item => {
    // Iterate over the roles of each user
    item.roles.forEach(role => {
      // If the role exists in the organizedData, push the user
      if (organizedData[role.name]) {
        organizedData[role.name].push(item.user)
      } else {
        // If the role doesn't exist, create a new array with the user
        organizedData[role.name] = [item.user]
      }
    })

    // Check if there are additional roles
    if (item.add_roles) {
      item.add_roles.forEach(role => {
        // If the role exists in the organizedData, push the user
        if (organizedData[role.name]) {
          organizedData[role.name].push(item.user)
        } else {
          // If the role doesn't exist, create a new array with the user
          organizedData[role.name] = [item.user]
        }
      })
    }
  })

  return organizedData
})

onBeforeMount(() => emit('aside-visible', false))
</script>

<template>
  <OverViewHeader :project="iProject" />

  <CRow class="mb-2">
    <CCol>{{ iProject?.description }}</CCol>
  </CRow>

  <CRow>
    <CCol lg="6">
      <CRow class="mb-3">
        <IssueTracker />
      </CRow>

      <CRow class="mb-3">
        <TimeSummary />
      </CRow>
    </CCol>

    <CCol lg="6">
      <MemberBox v-if="!!Object.keys(computedMembers).length" :project-memgers="computedMembers" />

      <SubProjects v-if="iProject?.sub_projects?.length" :sub-projects="iProject?.sub_projects" />
    </CCol>
  </CRow>
</template>
