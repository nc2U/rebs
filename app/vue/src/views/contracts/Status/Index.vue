<script lang="ts" setup>
import { computed, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { useContract } from '@/store/pinia/contract'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContSummary from '@/views/contracts/Status/components/ContSummary.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ContractBoard from '@/views/contracts/Status/components/ContractBoard.vue'

const projectStore = useProject()

const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)
const excelUrl = computed(() =>
  project.value ? `excel/status/?project=${project.value}` : '',
)

const projectDataStore = useProjectData()

const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)
const fetchBuildingList = (projId: number) =>
  projectDataStore.fetchBuildingList(projId)
const fetchHouseUnitList = (projId: number) =>
  projectDataStore.fetchHouseUnitList(projId)

const contractStore = useContract()
const contractsCount = computed(() => contractStore.contractsCount)
const fetchContractList = (payload: { project: number }) =>
  contractStore.fetchContractList(payload)
const fetchSubsSummaryList = (projId: number) =>
  contractStore.fetchSubsSummaryList(projId)

onMounted(() => {
  fetchTypeList(initProjId.value)
  fetchBuildingList(initProjId.value)
  fetchHouseUnitList(initProjId.value)
  fetchSubsSummaryList(initProjId.value)
  fetchContractList({ project: initProjId.value })
})

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchTypeList(target)
    fetchBuildingList(target)
    fetchHouseUnitList(target)
    fetchSubsSummaryList(target)
    fetchContractList({ project: target })
  } else {
    projectDataStore.unitTypeList = []
    projectDataStore.buildingList = []
    projectDataStore.houseUnitList = []
    contractStore.subsSummaryList = []
    contractStore.contractsCount = 0
  }
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContSummary :contracts-count="contractsCount" />
      <TableTitleRow v-if="project" excel :url="excelUrl" />
      <v-divider color="grey" class="my-0" />
      <ContractBoard />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
