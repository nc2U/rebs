<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { useContract } from '@/store/pinia/contract'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContSummary from '@/views/contracts/Status/components/ContSummary.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ContractBoard from '@/views/contracts/Status/components/ContractBoard.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const pDataStore = useProjectData()
const fetchTypeList = (projId: number) => pDataStore.fetchTypeList(projId)
const fetchBuildingList = (projId: number) =>
  pDataStore.fetchBuildingList(projId)
const fetchHouseUnitList = (projId: number) =>
  pDataStore.fetchHouseUnitList(projId)

const contStore = useContract()
const fetchContractList = (payload: { project: number }) =>
  contStore.fetchContractList(payload)
const fetchSubsSummaryList = (projId: number) =>
  contStore.fetchSubsSummaryList(projId)
const fetchContSummaryList = (projId: number) =>
  contStore.fetchContSummaryList(projId)

const excelUrl = computed(() =>
  project.value ? `excel/status/?project=${project.value}` : '',
)

const dataSetup = (pk: number) => {
  fetchTypeList(pk)
  fetchBuildingList(pk)
  fetchHouseUnitList(pk)
  fetchSubsSummaryList(pk)
  fetchContractList({ project: pk })
  fetchContSummaryList(pk)
}

const dataReset = () => {
  pDataStore.unitTypeList = []
  pDataStore.buildingList = []
  pDataStore.houseUnitList = []
  contStore.subsSummaryList = []
  contStore.contSummaryList = []
  contStore.contractsCount = 0
}

const projSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

onBeforeMount(() => dataSetup(project.value || projStore.initProjId))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @proj-select="projSelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContSummary />
      <TableTitleRow excel :url="excelUrl" :disabled="!project" />
      <v-divider color="grey" class="my-0" />
      <ContractBoard />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
