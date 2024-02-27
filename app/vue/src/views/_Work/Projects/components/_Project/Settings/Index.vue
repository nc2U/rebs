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
const taskProject = computed(() => workStore.taskProject)
const AllTaskProjects = computed(() => workStore.AllTaskProjects)

const onSubmit = (payload: any) => {
  payload.company = company?.value.pk
  if (!!payload.pk) workStore.updateTaskProject(payload)
  else workStore.createTaskProject(payload)
  console.log(payload)
}

onBeforeRouteUpdate(async to => {
  if (to.params.projId) await workStore.fetchTaskProject(to.params.projId as string)
  else {
    workStore.taskProject = null
    await workStore.fetchTaskProjectList()
  }
})

const route = useRoute()
onBeforeMount(() => {
  workStore.fetchTaskProjectList()
  if (route.params.projId) workStore.fetchTaskProject(route.params.projId as string)
})
</script>

<template>
  <ProjectForm
    title="설정"
    :project="taskProject"
    :all-task-projects="AllTaskProjects"
    @on-submit="onSubmit"
  />
</template>
