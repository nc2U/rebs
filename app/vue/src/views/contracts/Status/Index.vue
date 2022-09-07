<script lang="ts" setup>
import { computed, onMounted } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin'
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

onMounted(() => {
  fetchTypeList(initProjId.value)
  fetchBuildingList(initProjId.value)
  fetchHouseUnitList(initProjId.value)
})

const onSelectAdd = (target: any) => {
  if (target !== '') {
    fetchTypeList(target)
    fetchBuildingList(target)
    fetchHouseUnitList(target)
  } else {
    projectDataStore.unitTypeList = []
    projectDataStore.buildingList = []
    projectDataStore.houseUnitList = []
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
      <ContSummary />
      <TableTitleRow v-if="project" excel :url="excelUrl" />
      <v-divider color="grey" class="my-0" />
      <ContractBoard />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
