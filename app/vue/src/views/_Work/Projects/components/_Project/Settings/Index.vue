<script lang="ts" setup>
import { computed, inject, type ComputedRef, onBeforeMount } from 'vue'
import { useWork } from '@/store/pinia/work'
import type { Company } from '@/store/types/settings'
import ProjectForm from '@/views/_Work/Projects/components/_Project/ProjectForm.vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'

// const menus = ref([
//   '프로젝트',
//   '구성원',
//   '업무 추적',
//   '버전',
//   '업무 범주',
//   '저장소',
//   '게시판',
//   '시간 추적',
// ])

const company = inject<ComputedRef<Company>>('company')
const workStore = useWork()
const issueProject = computed(() => workStore.issueProject)
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
})
</script>

<template>
  <ProjectForm
    title="설정"
    :project="issueProject"
    :all-task-projects="AllIssueProjects"
    @on-submit="onSubmit"
  />
</template>
