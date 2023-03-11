<script lang="ts" setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { useContract, ContFilter } from '@/store/pinia/contract'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractSummary from './components/ContractSummary.vue'
import ListController from '@/views/contracts/List/components/ListController.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import SelectItems from '@/views/contracts/List/components/SelectItems.vue'
import ContractList from '@/views/contracts/List/components/ContractList.vue'

const listControl = ref()

const visible = ref(false)
const unitSet = ref(false)

const filteredStr = ref('')
const printItems = ref(['1', '2', '3', '4', '7', '8', '9', '11', '19-20-21-22'])

const childListFiltering = (page: number) =>
  listControl.value.listFiltering(page)

const projectStore = useProject()

const project = computed(() => projectStore.project)
const initProjId = computed(() => projectStore.initProjId)

watch(project, nVal => {
  if (nVal?.is_unit_set && !printItems.value.includes('5-6'))
    printItems.value.splice(4, 0, '5-6')
  unitSet.value = nVal?.is_unit_set || false
})

const excelUrl = computed(() => {
  const pk = project.value ? project.value.pk : ''
  const items = printItems.value.join('-')
  return `/excel/contracts/?project=${pk}${filteredStr.value}&col=${items}`
})

const contractStore = useContract()

const fetchOrderGroupList = (pk: number) =>
  contractStore.fetchOrderGroupList(pk)

const fetchContractList = (payload: ContFilter) =>
  contractStore.fetchContractList(payload)
const fetchSubsSummaryList = (pk: number) =>
  contractStore.fetchSubsSummaryList(pk)
const fetchContSummaryList = (pk: number) =>
  contractStore.fetchContSummaryList(pk)

const projectDataStore = useProjectData()

const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)
const fetchBuildingList = (projId: number) =>
  projectDataStore.fetchBuildingList(projId)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchOrderGroupList(target)
    fetchTypeList(target)
    fetchBuildingList(target)
    fetchContractList({ project: target })
    fetchSubsSummaryList(target)
    fetchContSummaryList(target)
  } else {
    contractStore.orderGroupList = []
    contractStore.subsSummaryList = []
    contractStore.contSummaryList = []
    contractStore.contractList = []
    contractStore.contractsCount = 0
    projectDataStore.buildingList = []
  }
}
const pageSelect = (page: number) => childListFiltering(page)

const onContFiltering = (payload: ContFilter) => {
  const {
    order_group,
    unit_type,
    building,
    status,
    null_unit,
    registed,
    from_date,
    to_date,
    search,
  } = payload
  payload.project = project.value?.pk
  const is_unit = null_unit ? '1' : ''
  const reg = registed === 'true' ? '1' : ''
  filteredStr.value = `&group=${order_group}&type=${unit_type}&dong=${building}&is_null=${is_unit}&reg=${reg}&status=${status}&sdate=${from_date}&edate=${to_date}&q=${search}`
  fetchContractList(payload)
}
const setItems = (arr: string[]) => (printItems.value = arr)

onMounted(() => {
  const projectPk = project.value?.pk || initProjId.value
  fetchOrderGroupList(projectPk)
  fetchTypeList(projectPk)
  fetchBuildingList(projectPk)
  fetchContractList({ project: projectPk })
  fetchSubsSummaryList(projectPk)
  fetchContSummaryList(projectPk)
})
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
      <TableTitleRow title="계약현황" excel :url="excelUrl">
        <v-btn
          size="small"
          rounded="pill"
          flat
          class="text-blue-accent-4"
          style="font-size: 0.95em"
          @click="visible = !visible"
        >
          [엑셀 출력항목 선택]
        </v-btn>
      </TableTitleRow>
      <SelectItems
        :visible="visible"
        :unit-set="unitSet"
        @print-items="setItems"
      />
      <ContractList @page-select="pageSelect" />
    </CCardBody>
    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
