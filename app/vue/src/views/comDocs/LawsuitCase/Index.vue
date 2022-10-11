<script setup lang="ts">
import { computed, onBeforeMount, onBeforeUpdate, reactive } from 'vue'
import { navMenu } from '@/views/comDocs/_menu/headermixin'
import { useRouter } from 'vue-router'
import { SuitCaseFilter as cFilter, useDocument } from '@/store/pinia/document'
import { SuitCase } from '@/store/types/document'
import HeaderNav from '@/components/HeaderNav.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CaseView from './components/CaseView.vue'
import CaseList from './components/CaseList.vue'
import CaseForm from './components/CaseForm.vue'

const caseFilter = reactive<cFilter>({
  page: 1,
  is_com: false,
  project: undefined,
  sort: undefined,
  level: undefined,
  court: '',
})

const listFiltering = (payload: cFilter) => {
  caseFilter.is_com = payload.is_com
  if (!payload.is_com) caseFilter.project = payload.project
  fetchSuitCaseList({ ...caseFilter })
}

const pageSelect = (page: number) => {
  caseFilter.page = page
  listFiltering(caseFilter)
}

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
const onSubmit = (payload: SuitCase) => {
  if (payload.pk) {
    updateSuitCase(payload)
    router.replace({
      name: '본사 소송사건 - 보기',
      params: { caseId: payload.pk },
    })
  } else {
    createSuitCase(payload)
    router.replace({ name: '본사 소송사건' })
  }
}

const onDelete = (pk: number) => deleteSuitCase(pk)

onBeforeMount(() => {
  fetchSuitCaseList({})
})

onBeforeUpdate(() => {
  fetchSuitCaseList({
    page: caseFilter.page,
  })
  fetchAllSuitCaseList({})
})
</script>

<template>
  <ContentBody>
    <CCardBody class="pb-5">
      <HeaderNav :menus="navMenu" />

      <div v-if="$route.name === '본사 소송사건'" class="pt-3">
        <ListController @list-filter="listFiltering" />

        <CaseList
          :page="caseFilter.page"
          :case-list="suitcaseList"
          @page-select="pageSelect"
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
