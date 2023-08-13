<script lang="ts" setup>
import { ref, computed, watch, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { useContract, type ContFilter } from '@/store/pinia/contract'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractSummary from './components/ContractSummary.vue'
import ListController from '@/views/contracts/List/components/ListController.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import SelectItems from '@/views/contracts/List/components/SelectItems.vue'
import ContractList from '@/views/contracts/List/components/ContractList.vue'

const status = ref('2')
const listControl = ref()

const visible = ref(false)
const unitSet = ref(false)

const filteredStr = ref('')
const printItems = ref(['1', '2', '4', '5', '8', '9', '10', '11'])

const projStore = useProject()
const project = computed(() => projStore.project)
watch(project, nVal => {
  unitSet.value = nVal?.is_unit_set || false
  if (!!nVal)
    if (nVal?.is_unit_set && !printItems.value.includes('6-7')) printItems.value.splice(4, 0, '6-7')
})

const excelUrl = computed(() => {
  const pk = project.value ? project.value?.pk : ''
  const items = printItems.value.join('-')
  return `/excel/contracts/?project=${pk}${filteredStr.value}&col=${items}`
})

const contStore = useContract()

const fetchOrderGroupList = (pk: number) => contStore.fetchOrderGroupList(pk)

const fetchContractList = (payload: ContFilter) => contStore.fetchContractList(payload)
const fetchSubsSummaryList = (pk: number) => contStore.fetchSubsSummaryList(pk)
const fetchContSummaryList = (pk: number) => contStore.fetchContSummaryList(pk)

const proDataStore = useProjectData()

const fetchTypeList = (projId: number) => proDataStore.fetchTypeList(projId)
const fetchBuildingList = (projId: number) => proDataStore.fetchBuildingList(projId)

const pageSelect = (page: number) => listControl.value.listFiltering(page)

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
  filteredStr.value = `&status=${status}&group=${order_group}&type=${unit_type}&dong=${building}&is_null=${is_unit}&reg=${reg}&status=${status}&sdate=${from_date}&edate=${to_date}&q=${search}`
  if (payload.project) fetchContractList(payload)
}
const setItems = (arr: string[]) => (printItems.value = arr)

const dataSetup = (proj: number) => {
  fetchOrderGroupList(proj)
  fetchTypeList(proj)
  fetchBuildingList(proj)
  fetchContractList({ project: proj })
  fetchSubsSummaryList(proj)
  fetchContSummaryList(proj)
}

const dataReset = () => {
  contStore.orderGroupList = []
  contStore.subsSummaryList = []
  contStore.contSummaryList = []
  contStore.contractList = []
  contStore.contractsCount = 0
  proDataStore.buildingList = []
}

const projSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

const [route, router] = [useRoute(), useRouter()]
onBeforeMount(() => {
  if (route.query?.status) {
    router.replace({ name: '계약 내역 조회' })
    status.value = '1'
  }
  dataSetup(project.value?.pk || projStore.initProjId)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" @proj-select="projSelect">
    <ContractSummary :project="project ?? undefined" />
  </ContentHeader>

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" :status="status" @cont-filtering="onContFiltering" />
      <TableTitleRow title="계약현황" excel :url="excelUrl" :disabled="!project">
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
      <SelectItems :visible="visible" :unit-set="unitSet" @print-items="setItems" />
      <ContractList @page-select="pageSelect" />
    </CCardBody>
    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
