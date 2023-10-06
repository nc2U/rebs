<script lang="ts" setup>
import { ref, computed, watch, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/proDocs/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { type RouteLocationNormalizedLoaded as LoadedRoute, useRoute, useRouter } from 'vue-router'
import { type SuitCaseFilter as cFilter, useDocument } from '@/store/pinia/document'
import type { AFile, Link, SuitCase } from '@/store/types/document'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/components/LawSuitCase/ListController.vue'
import CaseView from '@/components/LawSuitCase/CaseView.vue'
import CaseList from '@/components/LawSuitCase/CaseList.vue'
import CaseForm from '@/components/LawSuitCase/CaseForm.vue'

const fController = ref()
const mainViewName = ref('현장 소송 사건')
const caseFilter = ref<cFilter>({
  company: '',
  project: '',
  is_com: false,
  court: '',
  related_case: '',
  sort: '',
  level: '',
  in_progress: true,
  search: '',
  page: 1,
})

const listFiltering = (payload: cFilter) => {
  payload.is_com = false
  payload.project = project.value ?? ''
  caseFilter.value = payload
  if (company.value) fetchSuitCaseList({ ...caseFilter.value })
}

const pageSelect = (page: number) => {
  caseFilter.value.page = page
  listFiltering(caseFilter.value)
}

const projStore = useProject()
const project = computed(() => projStore.project?.pk)
const projName = computed(() => projStore.project?.name)
const company = computed(() => projStore.project?.company)

const docStore = useDocument()
const suitcase = computed(() => docStore.suitcase)
const suitcaseList = computed(() => docStore.suitcaseList)
const getSuitCase = computed(() => docStore.getSuitCase)

const fetchLink = (pk: number) => docStore.fetchLink(pk)
const fetchFile = (pk: number) => docStore.fetchFile(pk)
const fetchSuitCase = (pk: number) => docStore.fetchSuitCase(pk)
const fetchSuitCaseList = (payload: cFilter) => docStore.fetchSuitCaseList(payload)
const fetchAllSuitCaseList = (payload: cFilter) => docStore.fetchAllSuitCaseList(payload)

const createSuitCase = (payload: SuitCase & { isProject?: boolean }) =>
  docStore.createSuitCase(payload)
const updateSuitCase = (payload: SuitCase) => docStore.updateSuitCase(payload)
const deleteSuitCase = (pk: number) => docStore.deleteSuitCase(pk)
const patchLink = (payload: Link) => docStore.patchLink(payload)
const patchFile = (payload: AFile) => docStore.patchFile(payload)
const linkHit = async (pk: number) => {
  const link = (await fetchLink(pk)) as Link
  link.hit = (link.hit as number) + 1
  await patchLink(link)
}
const fileHit = async (pk: number) => {
  const file = (await fetchFile(pk)) as AFile
  file.hit = (file.hit as number) + 1
  await patchFile(file)
}

const [route, router] = [useRoute() as LoadedRoute & { name: string }, useRouter()]

watch(route, val => {
  if (val.params.caseId) fetchSuitCase(Number(val.params.caseId))
  else docStore.suitcase = null
})

const casesRenewal = (page: number) => {
  caseFilter.value.page = page
  fetchSuitCaseList(caseFilter.value)
}

const onSubmit = (payload: SuitCase & { isProject?: boolean }) => {
  payload.company = company.value ?? null
  payload.project = project.value ?? null

  if (payload.pk) {
    updateSuitCase(payload)
    router.replace({
      name: `${mainViewName.value} - 보기`,
      params: { caseId: payload.pk },
    })
  } else {
    payload.company = company.value || null
    payload.isProject = true
    createSuitCase(payload)
    router.replace({ name: `${mainViewName.value}` })
  }
}

const onDelete = (pk: number) => deleteSuitCase(pk)

const agencyFilter = (court: string) => {
  fController.value.courtChange(court)
  caseFilter.value.page = 1
  caseFilter.value.court = court
  listFiltering(caseFilter.value)
}
const agencySearch = (agent: string) => {
  fController.value.searchChange(agent)
  caseFilter.value.page = 1
  caseFilter.value.search = agent
  listFiltering(caseFilter.value)
}

const relatedFilter = (related: number) => {
  fController.value.relatedChange(related)
  caseFilter.value.page = 1
  caseFilter.value.related_case = related
  listFiltering(caseFilter.value)
}

const sortFilter = (project: number | null) => {
  fController.value.projectChange(project)
  caseFilter.value.page = 1
  if (project !== null) caseFilter.value.project = project
  else caseFilter.value.is_com = true
  listFiltering(caseFilter.value)
}

const dataSetup = (pk: number, caseId?: string | string[]) => {
  caseFilter.value.company = company.value ?? ''
  caseFilter.value.project = pk ?? ''
  fetchSuitCaseList(caseFilter.value)
  if (caseId) fetchSuitCase(Number(caseId))
  caseFilter.value.project = pk
}

const dataReset = () => {
  // projStore.project = null
  docStore.suitcaseList = []
  docStore.suitcaseCount = 0
  caseFilter.value.project = ''
  router.replace({ name: `${mainViewName.value}` })
}

const projSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

onBeforeMount(() => {
  const com = company.value ?? ''
  const proj = project.value || projStore.initProjId
  fetchAllSuitCaseList({ company: com, is_com: false, project: proj })
  dataSetup(proj, route.params?.caseId)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" @proj-select="projSelect" />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="route.name === `${mainViewName}`" class="pt-3">
        <ListController ref="fController" :case-filter="caseFilter" @list-filter="listFiltering" />

        <CaseList
          :company="company || undefined"
          :page="caseFilter.page ?? 1"
          :case-list="suitcaseList"
          :view-route="mainViewName"
          @page-select="pageSelect"
          @agency-filter="agencyFilter"
          @agency-search="agencySearch"
          @related-filter="relatedFilter"
          @sort-filter="sortFilter"
        />
      </div>

      <div v-else-if="route.name.includes('보기')">
        <CaseView
          :curr-page="caseFilter.page ?? 1"
          :suitcase="suitcase as SuitCase"
          :view-route="mainViewName"
          @link-hit="linkHit"
          @file-hit="fileHit"
          @cases-renewal="casesRenewal"
        />
      </div>

      <div v-else-if="route.name.includes('작성')">
        <CaseForm
          :sort-name="projName"
          :get-suit-case="getSuitCase"
          :view-route="mainViewName"
          @on-submit="onSubmit"
        />
      </div>

      <div v-else-if="route.name.includes('수정')">
        <CaseForm
          :sort-name="projName"
          :get-suit-case="getSuitCase"
          :suitcase="suitcase"
          :view-route="mainViewName"
          @on-submit="onSubmit"
          @on-delete="onDelete"
        />
      </div>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
