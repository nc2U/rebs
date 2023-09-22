<script setup lang="ts">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/comDocs/_menu/headermixin2'
import { type RouteLocationNormalizedLoaded as LoadedRoute, useRoute, useRouter } from 'vue-router'
import { useCompany } from '@/store/pinia/company'
import { type SuitCaseFilter as cFilter, useDocument } from '@/store/pinia/document'
import { type SuitCase } from '@/store/types/document'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CaseView from './components/CaseView.vue'
import CaseList from './components/CaseList.vue'
import CaseForm from './components/CaseForm.vue'

const fController = ref()
const caseFilter = ref<cFilter>({
  company: null,
  project: null,
  is_com: '',
  court: '',
  related_case: '',
  sort: '',
  level: '',
  search: '',
  page: 1,
})

const listFiltering = (payload: cFilter) => {
  caseFilter.value = payload
  caseFilter.value.project = payload.is_com ? null : payload.project
  if (company.value) fetchSuitCaseList({ ...caseFilter.value })
}

const pageSelect = (page: number) => {
  caseFilter.value.page = page
  listFiltering(caseFilter.value)
}

const comStore = useCompany()
const company = computed(() => comStore.company?.pk)

const docStore = useDocument()
const suitcase = computed(() => docStore.suitcase)
const suitcaseList = computed(() => docStore.suitcaseList)
const getSuitCase = computed(() => docStore.getSuitCase)

const fetchSuitCase = (pk: number) => docStore.fetchSuitCase(pk)
const fetchSuitCaseList = (payload: cFilter) => docStore.fetchSuitCaseList(payload)
const fetchAllSuitCaseList = (payload: cFilter) => docStore.fetchAllSuitCaseList(payload)

const createSuitCase = (payload: SuitCase) => docStore.createSuitCase(payload)
const updateSuitCase = (payload: SuitCase) => docStore.updateSuitCase(payload)
const deleteSuitCase = (pk: number) => docStore.deleteSuitCase(pk)

const [route, router] = [useRoute() as LoadedRoute & { name: string }, useRouter()]

watch(route, val => {
  if (val.params.caseId) fetchSuitCase(Number(val.params.caseId))
  else docStore.suitcase = null
})

const onSubmit = (payload: SuitCase) => {
  if (!!company.value)
    if (payload.pk) {
      updateSuitCase(payload)
      router.replace({
        name: '본사 소송 사건 - 보기',
        params: { caseId: payload.pk },
      })
    } else {
      payload.company = company.value || null
      createSuitCase(payload)
      router.replace({ name: '본사 소송 사건' })
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
  fetchSuitCaseList({ company: pk, page: caseFilter.value.page })
  if (caseId) fetchSuitCase(Number(caseId))
}

const dataReset = () => {
  comStore.company = null
  docStore.suitcaseList = []
  docStore.suitcaseCount = 0
  router.replace({ name: '본사 소송 사건' })
}

const comSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

onBeforeMount(() => {
  fetchAllSuitCaseList({})
  dataSetup(company.value || comStore.initComId, route.params?.caseId)
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="CompanySelect"
    @com-select="comSelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="route.name === '본사 소송 사건'" class="pt-3">
        <ListController ref="fController" @list-filter="listFiltering" />

        <CaseList
          :company="company || undefined"
          :page="caseFilter.page"
          :case-list="suitcaseList"
          @page-select="pageSelect"
          @agency-filter="agencyFilter"
          @agency-search="agencySearch"
          @related-filter="relatedFilter"
          @sort-filter="sortFilter"
        />
      </div>

      <div v-else-if="route.name.includes('보기')">
        <CaseView :suitcase="suitcase as SuitCase" />
      </div>

      <div v-else-if="route.name.includes('작성')">
        <CaseForm :get-suit-case="getSuitCase" @on-submit="onSubmit" />
      </div>

      <div v-else-if="route.name.includes('수정')">
        <CaseForm
          :get-suit-case="getSuitCase"
          :suitcase="suitcase"
          @on-submit="onSubmit"
          @on-delete="onDelete"
        />
      </div>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
