<script lang="ts" setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { useContract } from '@/store/pinia/contract'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin'
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
const printItems = ref(['1', '2', '3', '4', '7', '8', '9', '10', '18-19-20-21'])

const childListFiltering = (page: number) =>
  listControl.value.listFiltering(page)

const store = useStore()
const projectStore = useProject()

const project = computed(() => projectStore.project)
const initProjId = computed(() => projectStore.initProjId)

watch(project, nVal => {
  if (nVal?.is_unit_set) printItems.value.splice(4, 0, '5-6')
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

const fetchContractList = (project: { project: number }) =>
  contractStore.fetchContractList(project)
const fetchSubsSummaryList = (pk: number) =>
  contractStore.fetchSubsSummaryList(pk)
const fetchContSummaryList = (pk: number) =>
  contractStore.fetchContSummaryList(pk)

const pData = useProjectData()

const fetchTypeList = (projId: number) => pData.fetchTypeList(projId)
const fetchBuildingList = (projId: number) => pData.fetchBuildingList(projId)

const onSelectAdd = (target: any) => {
  if (target !== '') {
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
    pData.buildingList = []
  }
}
const pageSelect = (page: number) => childListFiltering(page)
const onContFiltering = (payload: any) => {
  const pk = project.value?.pk
  const {
    order_group,
    unit_type,
    building,
    status,
    registed,
    from_date,
    to_date,
    search,
  } = payload
  const reg = registed === 'true' ? '1' : ''
  filteredStr.value = `&group=${order_group}&type=${unit_type}&dong=${building}&status=${status}&reg=${reg}&sdate=${from_date}&edate=${to_date}&q=${search}`
  fetchContractList({ ...{ project: pk }, ...payload })
}
const setItems = (arr: string[]) => (printItems.value = arr)

onMounted(() => {
  fetchOrderGroupList(initProjId.value)
  fetchTypeList(initProjId.value)
  fetchBuildingList(initProjId.value)
  fetchContractList({ project: initProjId.value })
  fetchSubsSummaryList(initProjId.value)
  fetchContSummaryList(initProjId.value)
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
        :project="unitSet"
        @print-items="setItems"
      />
      <ContractList @page-select="pageSelect" />
    </CCardBody>
    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
