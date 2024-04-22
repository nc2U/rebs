<script setup lang="ts">
import { ref, computed, onBeforeMount, provide, inject, type ComputedRef } from 'vue'
import { navMenu1, navMenu2 } from '@/views/_Work/_menu/headermixin1'
import { useWork } from '@/store/pinia/work'
import { useAccount } from '@/store/pinia/account'
import { onBeforeRouteUpdate, useRoute, useRouter } from 'vue-router'
import type { Company } from '@/store/types/settings'
import type { ActLogEntryFilter } from '@/store/types/work'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import ProjectList from '@/views/_Work/Manages/Projects/components/ProjectList.vue'
import ProjectForm from '@/views/_Work/Manages/Projects/components/ProjectForm.vue'
import Overview from '@/views/_Work/Manages/Projects/components/Overview/Index.vue'
import Activity from '@/views/_Work/Manages/Projects/components/Activity/Index.vue'
import Roadmap from '@/views/_Work/Manages/Projects/components/Roadmap/Index.vue'
import Issues from '@/views/_Work/Manages/Projects/components/Issues/Index.vue'
import SpentTime from '@/views/_Work/Manages/Projects/components/SpentTime/Index.vue'
import Gantt from '@/views/_Work/Manages/Projects/components/Gantt/Index.vue'
import Calendar from '@/views/_Work/Manages/Projects/components/Calendar/Index.vue'
import News from '@/views/_Work/Manages/Projects/components/News/Index.vue'
import Documents from '@/views/_Work/Manages/Projects/components/Documents/Index.vue'
import Wiki from '@/views/_Work/Manages/Projects/components/Wiki/Index.vue'
import Forums from '@/views/_Work/Manages/Projects/components/Forums/Index.vue'
import Files from '@/views/_Work/Manages/Projects/components/Files/Index.vue'
import Repository from '@/views/_Work/Manages/Projects/components/Repository/Index.vue'
import Settings from '@/views/_Work/Manages/Projects/components/Settings/Index.vue'
import AsideActivity from '@/views/_Work/Manages/Activity/components/aside/AsideActivity.vue'
import ActivityLogList from '@/views/_Work/Manages/Activity/components/ActivityLogList.vue'

const cBody = ref()
const aside = ref(true)

const asideVisible = (visible: boolean) => (aside.value = visible)

const [route, router] = [useRoute(), useRouter()]

const routeName = computed(() => route.name as string)
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)
const headerTitle = computed(() =>
  routeName.value.includes('프로젝트') ? comName.value : issueProject.value?.name,
)

const accStore = useAccount()
const superAuth = computed(() => accStore.superAuth)

const workStore = useWork()
const issueProject = computed(() => workStore.issueProject)
provide('iProject', issueProject)
const issueProjects = computed(() => workStore.issueProjects)
const allProjects = computed(() => workStore.AllIssueProjects)

const version = computed(() => false)
const modules = computed(() => issueProject.value?.module)

const navMenus = computed(() => (!issueProjects.value.length ? navMenu1 : navMenu2))

const projectNavMenus = computed(() => {
  let menus = [
    { no: 1, menu: '(개요)' },
    { no: 2, menu: '(작업내역)' },
  ]
  if (version.value) menus = [...new Set([...menus, ...[{ no: 3, menu: '(로드맵)' }]])]
  if (modules.value?.issue) menus = [...new Set([...menus, ...[{ no: 4, menu: '(업무)' }]])]
  if (modules.value?.time) menus = [...new Set([...menus, ...[{ no: 5, menu: '(소요시간)' }]])]
  if (modules.value?.gantt) menus = [...new Set([...menus, ...[{ no: 6, menu: '(차트)' }]])]
  if (modules.value?.calendar) menus = [...new Set([...menus, ...[{ no: 7, menu: '(달력)' }]])]
  if (modules.value?.news) menus = [...new Set([...menus, ...[{ no: 8, menu: '(공지)' }]])]
  if (modules.value?.document) menus = [...new Set([...menus, ...[{ no: 9, menu: '(문서)' }]])]
  if (modules.value?.wiki) menus = [...new Set([...menus, ...[{ no: 10, menu: '(위키)' }]])]
  if (modules.value?.file) menus = [...new Set([...menus, ...[{ no: 11, menu: '(파일)' }]])]
  if (superAuth.value) menus = [...menus, ...[{ no: 12, menu: '(설정)' }]]

  return menus.sort((a, b) => a.no - b.no).map(m => m.menu)
})

const navMenu = computed(() =>
  routeName.value.includes('프로젝트') ? navMenus.value : projectNavMenus.value,
)

const sideNavCAll = () => cBody.value.toggle()

const onSubmit = (payload: any) => {
  payload.company = company?.value.pk
  workStore.createIssueProject(payload)
  setTimeout(() => {
    router.push({
      name: '(설정)',
      params: { projId: issueProject.value?.slug },
    })
  }, 500)
}

const filteringProject = (payload: any) => {
  console.log(payload)
  workStore.fetchIssueProjectList(payload)
}

const toDate = ref(new Date())

const toBack = (date: Date) => (toDate.value = date)
const toNext = (date: Date) => (toDate.value = date)

const filterActivity = (payload: ActLogEntryFilter) => {
  console.log(payload)
  if (payload.to_act_date) toDate.value = payload.to_act_date
  workStore.fetchActivityLogList(payload)
}

onBeforeRouteUpdate(async to => {
  if (to.params.projId) await workStore.fetchIssueProject(to.params.projId as string)
  else workStore.issueProject = null
})

onBeforeMount(async () => {
  await workStore.fetchIssueProjectList({})
  await workStore.fetchAllIssueProjectList()
  if (route.params.projId) await workStore.fetchIssueProject(route.params.projId as string)
})
</script>

<template>
  <Header
    :page-title="headerTitle"
    :nav-menu="navMenu"
    :family-tree="issueProject?.family_tree"
    @side-nav-call="sideNavCAll"
  />
  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query" :aside="aside">
    <template v-slot:default>
      <ProjectList
        v-if="routeName === '프로젝트'"
        :project-list="issueProjects"
        :all-projects="allProjects"
        @aside-visible="asideVisible"
        @filter-submit="filteringProject"
      />

      <ProjectForm
        v-if="routeName === '프로젝트 - 추가'"
        title="새 프로젝트"
        :all-projects="allProjects"
        @aside-visible="asideVisible"
        @on-submit="onSubmit"
      />

      <Overview v-if="routeName === '(개요)'" @aside-visible="asideVisible" />

      <Activity
        v-if="routeName === '(작업내역)'"
        :to-date="toDate"
        @to-back="toBack"
        @to-next="toNext"
        @aside-visible="asideVisible"
      />

      <Roadmap v-if="routeName === '(로드맵)'" @aside-visible="asideVisible" />

      <Issues v-if="routeName.includes('(업무)')" @aside-visible="asideVisible" />

      <SpentTime v-if="routeName.includes('(소요시간)')" @aside-visible="asideVisible" />

      <Gantt v-if="routeName === '(차트)'" @aside-visible="asideVisible" />

      <Calendar v-if="routeName === '(달력)'" @aside-visible="asideVisible" />

      <News v-if="routeName === '(공지)'" @aside-visible="asideVisible" />

      <Documents v-if="routeName === '(문서)'" @aside-visible="asideVisible" />

      <Wiki v-if="routeName === '(위키)'" @aside-visible="asideVisible" />

      <Forums v-if="routeName === '(게시판)'" @aside-visible="asideVisible" />

      <Files v-if="routeName === '(파일)'" @aside-visible="asideVisible" />

      <Repository v-if="routeName === '(저장소)'" @aside-visible="asideVisible" />

      <Settings v-if="routeName === '(설정)'" @aside-visible="asideVisible" />
    </template>

    <template v-slot:aside>
      <AsideActivity
        v-if="routeName === '(작업내역)'"
        :has-subs="!!issueProject?.sub_projects?.length"
        @filter-activity="filterActivity"
      />
    </template>
  </ContentBody>
</template>
