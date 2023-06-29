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
const project = computed(() => projStore.project?.pk || projStore.initProjId)

const excelUrl = computed(() =>
  project.value ? `excel/status/?project=${project.value}` : '',
)

const pDataStore = useProjectData()

const fetchTypeList = (projId: number) => pDataStore.fetchTypeList(projId)
const fetchBuildingList = (projId: number) =>
  pDataStore.fetchBuildingList(projId)
const fetchHouseUnitList = (projId: number) =>
  pDataStore.fetchHouseUnitList(projId)

const contStore = useContract()
const contractsCount = computed(() => contStore.contractsCount)
const fetchContractList = (payload: { project: number }) =>
  contStore.fetchContractList(payload)
const fetchSubsSummaryList = (projId: number) =>
  contStore.fetchSubsSummaryList(projId)
const fetchContSummaryList = (projId: number) =>
  contStore.fetchContSummaryList(projId)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchTypeList(target)
    fetchBuildingList(target)
    fetchHouseUnitList(target)
    fetchSubsSummaryList(target)
    fetchContractList({ project: target })
    fetchContSummaryList(target)
  } else {
    pDataStore.unitTypeList = []
    pDataStore.buildingList = []
    pDataStore.houseUnitList = []
    contStore.subsSummaryList = []
    contStore.contSummaryList = []
    contStore.contractsCount = 0
  }
  pDataStore.isLoading = true
}

onBeforeMount(() => {
  const projectPk = project.value
  fetchTypeList(projectPk)
  fetchBuildingList(projectPk)
  fetchHouseUnitList(projectPk)
  fetchSubsSummaryList(projectPk)
  fetchContractList({ project: projectPk })
  fetchContSummaryList(projectPk)
})
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
      <TableTitleRow excel :url="excelUrl" :disabled="!project" />
      <v-divider color="grey" class="my-0" />
      <ContractBoard />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
