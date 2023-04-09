<script setup lang="ts">
import { ref, computed, onBeforeMount, onBeforeUpdate } from 'vue'
import { pageTitle, navMenu } from '@/views/comDocs/_menu/headermixin2'
import { useRouter } from 'vue-router'
import { useCompany } from '@/store/pinia/company'
import { SuitCaseFilter as cFilter, useDocument } from '@/store/pinia/document'
import { SuitCase } from '@/store/types/document'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CaseView from './components/CaseView.vue'
import CaseList from './components/CaseList.vue'
import CaseForm from './components/CaseForm.vue'

const fController = ref()
const caseFilter = ref<cFilter>({
  company: null,
  project: '',
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
  caseFilter.value.project = payload.is_com ? '' : payload.project
  if (company.value) fetchSuitCaseList({ ...caseFilter.value })
}

const pageSelect = (page: number) => {
  caseFilter.value.page = page
  listFiltering(caseFilter.value)
}

const comStore = useCompany()
const initComId = computed(() => comStore.initComId)
const company = computed(() => comStore.company?.pk || null)

const documentStore = useDocument()
const suitcaseList = computed(() => documentStore.suitcaseList)

const fetchSuitCaseList = (payload: cFilter) =>
  documentStore.fetchSuitCaseList(payload)
const fetchAllSuitCaseList = (payload: cFilter) =>
  documentStore.fetchAllSuitCaseList(payload)

const createSuitCase = (payload: SuitCase) =>
  documentStore.createSuitCase(payload)
const updateSuitCase = (payload: SuitCase) =>
  documentStore.updateSuitCase(payload)
const deleteSuitCase = (pk: number) => documentStore.deleteSuitCase(pk)

const router = useRouter()

const companySelect = (target: number) => {
  if (!!target) {
    fetchSuitCaseList({ company: target })
  } else {
    comStore.company = null
    documentStore.suitcaseList = []
    documentStore.suitcaseCount = 0
    router.replace({ name: '본사 소송 사건' })
  }
}

const onSubmit = (payload: SuitCase) => {
  if (payload.pk) {
    updateSuitCase(payload)
    router.replace({
      name: '본사 소송 사건 - 보기',
      params: { caseId: payload.pk },
    })
  } else {
    payload.company = company.value
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

onBeforeMount(() => {
  if (initComId.value) fetchSuitCaseList({ company: initComId.value })
  fetchAllSuitCaseList({})
})

onBeforeUpdate(() => {
  if (company.value)
    fetchSuitCaseList({ company: company.value, page: caseFilter.value.page })
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="companySelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="$route.name === '본사 소송 사건'" class="pt-3">
        <ListController ref="fController" @list-filter="listFiltering" />

        <CaseList
          :company="company"
          :page="caseFilter.page"
          :case-list="suitcaseList"
          @page-select="pageSelect"
          @agency-filter="agencyFilter"
          @agency-search="agencySearch"
          @related-filter="relatedFilter"
          @sort-filter="sortFilter"
        />
      </div>

      <div v-else-if="$route.name.includes('보기')">
        <CaseView />
      </div>

      <div v-else-if="$route.name.includes('작성')">
        <CaseForm @on-submit="onSubmit" />
      </div>

      <div v-else-if="$route.name.includes('수정')">
        <CaseForm @on-submit="onSubmit" @on-delete="onDelete" />
      </div>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
