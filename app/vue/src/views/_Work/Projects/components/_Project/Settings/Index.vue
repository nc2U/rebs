<script lang="ts" setup="">
import { ref, computed, inject, type ComputedRef } from 'vue'
import { useWork } from '@/store/pinia/work'
import type { Company } from '@/store/types/settings'
import ProjectForm from '@/views/_Work/Projects/components/_Project/ProjectForm.vue'

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
</script>

<template>
  <ProjectForm
    title="설정"
    :project="taskProject"
    :all-task-projects="AllTaskProjects"
    @on-submit="onSubmit"
  >
    <!--    <CNav variant="tabs" class="mb-3 pl-4">-->
    <!--      <CNavItem v-for="(menu, i) in menus" :key="i">-->
    <!--        <CNavLink-->
    <!--          :active="-->
    <!--            ($route.name as string).includes(menu as string) ||-->
    <!--            ($route.meta.title as string).includes(menu as string)-->
    <!--          "-->
    <!--          @click="$router.push({ name: menu as RouteRecordName, query })"-->
    <!--        >-->
    <!--          {{ menu }}-->
    <!--        </CNavLink>-->
    <!--      </CNavItem>-->
    <!--    </CNav>-->
  </ProjectForm>
</template>
