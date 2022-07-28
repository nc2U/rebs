<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractSummary from './components/ContractSummary.vue'
import ListController from '@/views/contracts/List/components/ListController.vue'
import ExcelExport from '@/components/DownLoad/ExcelExport.vue'
import ContractList from '@/views/contracts/List/components/ContractList.vue'

const store = useStore()

const listControl = ref()
const childListFiltering = (page: number) =>
  listControl.value.listFiltering(page)

const project = computed(() => store.state.project.project)
const initProjId = computed(() => store.getters['accounts/initProjId'])

const fetchOrderGroupList = (id: number) =>
  store.dispatch('contract/fetchOrderGroupList', id)
const fetchContractList = (project: { project: number }) =>
  store.dispatch('contract/fetchContractList', project)
const fetchSubsSummaryList = (id: number) =>
  store.dispatch('contract/fetchSubsSummaryList', id)
const fetchContSummaryList = (id: number) =>
  store.dispatch('contract/fetchContSummaryList', id)

const fetchTypeList = (id: number) =>
  store.dispatch('project/fetchTypeList', id)
const fetchBuildingList = (id: number) =>
  store.dispatch('project/fetchBuildingList', id)

const contractUpdate = (payload: any) =>
  store.commit('contract/updateState', payload)
const projectUpdate = (payload: any) =>
  store.commit('project/updateState', payload)

onMounted(() => {
  fetchOrderGroupList(initProjId.value)
  fetchTypeList(initProjId.value)
  fetchBuildingList(initProjId.value)
  fetchContractList({ project: initProjId.value })
  fetchSubsSummaryList(initProjId.value)
  fetchContSummaryList(initProjId.value)
})

const onSelectAdd = (target: any) => {
  if (target !== '') {
    fetchOrderGroupList(target)
    fetchTypeList(target)
    fetchBuildingList(target)
    fetchContractList({ project: target })
    fetchSubsSummaryList(target)
    fetchContSummaryList(target)
  } else {
    contractUpdate({
      orderGroupList: [],
      subsSummaryList: [],
      contSummaryList: [],
      contractList: [],
      contractsCount: 0,
    })
    projectUpdate({ unitTypeList: [], buildingList: [] })
  }
}
const pageSelect = (page: number) => childListFiltering(page)
const onContFiltering = (payload: any) => {
  const pk: number = project.value.pk
  fetchContractList({ ...{ project: pk }, ...payload })
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  >
    <ContractSummary :project="project" />
  </ContentHeader>

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @cont-filtering="onContFiltering" />
      <ExcelExport v-if="project" url="" disabled />
      <ContractList @page-select="pageSelect" />
    </CCardBody>
    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
