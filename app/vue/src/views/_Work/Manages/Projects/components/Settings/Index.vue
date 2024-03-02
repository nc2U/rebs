<script lang="ts" setup>
import { ref, computed, inject, type ComputedRef, onBeforeMount } from 'vue'
import { useWork } from '@/store/pinia/work'
import type { Company } from '@/store/types/settings'
import ProjectForm from '@/views/_Work/Manages/Projects/components/ProjectForm.vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import Member from '@/views/_Work/Manages/Projects/components/Settings/components/Member.vue'
import IssueTracking from '@/views/_Work/Manages/Projects/components/Settings/components/IssueTracking.vue'
import Version from '@/views/_Work/Manages/Projects/components/Settings/components/Version.vue'
import IssueCategory from '@/views/_Work/Manages/Projects/components/Settings/components/IssueCategory.vue'
import Repository from '@/views/_Work/Manages/Projects/components/Settings/components/Repository.vue'
import Forum from '@/views/_Work/Manages/Projects/components/Settings/components/Forum.vue'
import TimeTracking from '@/views/_Work/Manages/Projects/components/Settings/components/TimeTracking.vue'

const emit = defineEmits(['aside-visible'])

const menu = ref('프로젝트')

const settingMenus = computed(() => {
  let menus = [
    { no: 1, menu: '프로젝트' },
    { no: 2, menu: '구성원' },
    { no: 4, menu: '버전' },
  ]

  if (modules.value?.issue)
    menus = [
      ...new Set([
        ...menus,
        ...[
          { no: 3, menu: '업무추적' },
          { no: 5, menu: '업무범주' },
        ],
      ]),
    ]
  if (modules.value?.time) menus = [...new Set([...menus, ...[{ no: 8, menu: '시간추적' }]])]
  if (modules.value?.repository) menus = [...new Set([...menus, ...[{ no: 6, menu: '저장소' }]])]
  if (modules.value?.forum) menus = [...new Set([...menus, ...[{ no: 7, menu: '게시판' }]])]

  return menus.sort((a, b) => a.no - b.no).map(m => m.menu)
})

const company = inject<ComputedRef<Company>>('company')
const workStore = useWork()
const issueProject = computed(() => workStore.issueProject)
const modules = computed(() => issueProject.value?.module)
const AllIssueProjects = computed(() => workStore.AllIssueProjects)

const onSubmit = (payload: any) => {
  payload.company = company?.value.pk
  if (!!payload.pk) workStore.updateIssueProject(payload)
  else workStore.createIssueProject(payload)
  console.log(payload)
}

onBeforeRouteUpdate(async to => {
  if (to.params.projId) await workStore.fetchIssueProject(to.params.projId as string)
  else {
    workStore.issueProject = null
    await workStore.fetchIssueProjectList()
  }
})

const route = useRoute()
onBeforeMount(() => {
  workStore.fetchIssueProjectList()
  if (route.params.projId) workStore.fetchIssueProject(route.params.projId as string)
  emit('aside-visible', false)
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>설정</h5>
    </CCol>
  </CRow>

  <CRow class="mb-3">
    <CCol>
      <v-tabs density="compact">
        <v-tab v-for="m in settingMenus" :value="m" :key="m" @click="menu = m">{{ m }}</v-tab>
      </v-tabs>
    </CCol>
  </CRow>

  <ProjectForm
    v-if="menu === '프로젝트'"
    :project="issueProject"
    :all-task-projects="AllIssueProjects"
    @on-submit="onSubmit"
  />

  <Member v-if="menu === '구성원'" />

  <IssueTracking v-if="menu === '업무추적'" />

  <Version v-if="menu === '버전'" />

  <IssueCategory v-if="menu === '업무범주'" />

  <Repository v-if="menu === '저장소'" />

  <Forum v-if="menu === '게시판'" />

  <TimeTracking v-if="menu === '시간추적'" />
</template>
