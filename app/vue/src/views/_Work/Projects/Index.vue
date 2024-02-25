<script setup lang="ts">
import { ref, computed, inject, onBeforeMount, type ComputedRef } from 'vue'
import { navMenu as navMenu1 } from '@/views/_Work/_menu/headermixin1'
import { navMenu as navMenu2 } from '@/views/_Work/_menu/headermixin2'
import type { Company } from '@/store/types/settings'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import { useWork } from '@/store/pinia/work'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import ProjectList from '@/views/_Work/Projects/components/_Project/ProjectList.vue'
import ProjectForm from '@/views/_Work/Projects/components/_Project/ProjectForm.vue'
import Overview from '@/views/_Work/Projects/components/_Project/Overview/Index.vue'
import Activity from '@/views/_Work/Projects/components/_Project/Activity/Index.vue'
import Roadmap from '@/views/_Work/Projects/components/_Project/Roadmap/Index.vue'
import Issues from '@/views/_Work/Projects/components/_Project/Issues/Index.vue'
import SpentTime from '@/views/_Work/Projects/components/_Project/SpentTime/Index.vue'
import Gantt from '@/views/_Work/Projects/components/_Project/Gantt/Index.vue'
import Calendar from '@/views/_Work/Projects/components/_Project/Calendar/Index.vue'
import News from '@/views/_Work/Projects/components/_Project/News/Index.vue'
import Documents from '@/views/_Work/Projects/components/_Project/Documents/Index.vue'
import Wiki from '@/views/_Work/Projects/components/_Project/Wiki/Index.vue'
import Forums from '@/views/_Work/Projects/components/_Project/Forums/Index.vue'
import Files from '@/views/_Work/Projects/components/_Project/Files/Index.vue'
import Repository from '@/views/_Work/Projects/components/_Project/Repository/Index.vue'
import Settings from '@/views/_Work/Projects/components/_Project/Settings/Index.vue'

const cBody = ref()

const route = useRoute()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)
const navMenu = computed(() => ((route.name as string).includes('프로젝트') ? navMenu1 : navMenu2))

const headerTitle = computed(() =>
  (route.name as string).includes('프로젝트') ? comName.value : taskProject.value?.name,
)

const sideNavCAll = () => cBody.value.toggle()

const workStore = useWork()
const taskProject = computed(() => workStore.taskProject)
const taskProjectList = computed(() => workStore.taskProjectList)
const getProjects = computed(() => workStore.getProjects)

const fetchTaskProjectList = () => workStore.fetchTaskProjectList()
const fetchTaskProject = (projId: string) => workStore.fetchTaskProject(projId)
const createTaskProject = (payload: any) => workStore.createTaskProject(payload)
const updateTaskProject = (payload: any) => workStore.updateTaskProject(payload)

const onSubmit = (payload: any) => {
  payload.company = company?.value.pk
  if (!!payload.pk) updateTaskProject(payload)
  else createTaskProject(payload)
}

onBeforeRouteUpdate(async to => {
  if (to.params.projId) await fetchTaskProject(to.params.projId[0])
  else {
    workStore.taskProject = null
    await fetchTaskProjectList()
  }
})

onBeforeMount(() => {
  workStore.fetchTaskProjectList()
  if (route.params.projId) fetchTaskProject(route.params.projId[0])
})
</script>

<template>
  <Header :page-title="headerTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <ProjectList v-if="route.name === '프로젝트'" :project-list="taskProjectList" />

      <ProjectForm
        v-if="route.name === '프로젝트 - 생성'"
        title="새 프로젝트"
        :get-projects="getProjects"
        @on-submit="onSubmit"
      />

      <Overview v-if="route.name === '(개요)'" />

      <Activity v-if="route.name === '(작업내역)'" />

      <Roadmap v-if="route.name === '(로드맵)'" />

      <Issues v-if="route.name === '(업무)'" />

      <SpentTime v-if="route.name === '(소요시간)'" />

      <Gantt v-if="route.name === '(차트)'" />

      <Calendar v-if="route.name === '(달력)'" />

      <News v-if="route.name === '(공지)'" />

      <Documents v-if="route.name === '(문서)'" />

      <Wiki v-if="route.name === '(위키)'" />

      <Forums v-if="route.name === '(게시판)'" />

      <Files v-if="route.name === '(파일)'" />

      <Repository v-if="route.name === '(저장소)'" />

      <Settings v-if="route.name === '(설정)'" />
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
