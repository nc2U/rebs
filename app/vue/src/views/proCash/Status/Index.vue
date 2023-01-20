<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useProCash } from '@/store/pinia/proCash'
import { dateFormat } from '@/utils/baseMixins'
import { pageTitle, navMenu } from '@/views/proCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/proCash/Status/components/DateChoicer.vue'
import TabSelect from '@/views/proCash/Status/components/TabSelect.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import StatusByAccount from '@/views/proCash/Status/components/StatusByAccount.vue'
import CashListByDate from '@/views/proCash/Status/components/CashListByDate.vue'
import SummaryForBudget from '@/views/proCash/Status/components/SummaryForBudget.vue'

const date = ref(new Date())
const compName = ref('StatusByAccount')

const projectStore = useProject()

const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const proCashStore = useProCash()
const fetchProAllAccD1List = () => proCashStore.fetchProAllAccD1List
const fetchProAllAccD2List = () => proCashStore.fetchProAllAccD2List
const fetchProBankAccList = (proj: number) =>
  proCashStore.fetchProBankAccList(proj)

const fetchBalanceByAccList = (payload: { project: number; date?: string }) =>
  proCashStore.fetchBalanceByAccList(payload)
const fetchDateCashBookList = (payload: { project: number; date: string }) =>
  proCashStore.fetchDateCashBookList(payload)
const fetchProjectBudgetList = (proj: number) =>
  proCashStore.fetchProjectBudgetList(proj)
const patchProBudgetList = (proj: number, pk: number, budget: number) =>
  proCashStore.patchProBudgetList(proj, pk, budget)
const fetchExecAmountList = (project: number, date?: string) =>
  proCashStore.fetchExecAmountList(project, date)

const excelUrl = computed(() => {
  const comp = compName.value
  const pj = project.value
  const dt = dateFormat(date.value)
  let url = ''
  if (comp === 'StatusByAccount') url = `/excel/p-balance/`
  else if (comp === 'CashListByDate') url = `/excel/p-daily-cash/`
  else if (comp === 'SummaryForBudget') url = `/excel/p-budget/`
  return `${url}?project=${pj}&date=${dt}`
})

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchProBankAccList(target)
    fetchBalanceByAccList({ project: target, date: dateFormat(date.value) })
    fetchDateCashBookList({
      project: target,
      date: dateFormat(date.value),
    })
    fetchProjectBudgetList(target)
    fetchExecAmountList(target, dateFormat(date.value))
  } else {
    proCashStore.proBankAccountList = []
    proCashStore.balanceByAccList = []
    proCashStore.proDateCashBook = []
    proCashStore.proBudgetList = []
    proCashStore.execAmountList = []
  }
}

const showTab = (num: number) => {
  const comp: { [key: number]: string } = {
    1: 'StatusByAccount',
    2: 'CashListByDate',
    3: 'SummaryForBudget',
  }
  compName.value = comp[num]
}

const setDate = (d: Date) => {
  const dt = new Date(d)
  date.value = dt
  fetchBalanceByAccList({ project: project.value, date: dateFormat(dt) })
  fetchDateCashBookList({ project: project.value, date: dateFormat(dt) })
  fetchProjectBudgetList(project.value)
  fetchExecAmountList(project.value, dateFormat(dt))
}

const patchBudget = (pk: number, budget: number) =>
  patchProBudgetList(project.value, pk, budget)

onBeforeMount(() => {
  fetchProAllAccD1List()
  fetchProAllAccD2List()
  fetchProBankAccList(initProjId.value)
  fetchBalanceByAccList({
    project: initProjId.value,
    date: dateFormat(date.value),
  })
  fetchDateCashBookList({
    project: initProjId.value,
    date: dateFormat(date.value),
  })
  fetchProjectBudgetList(initProjId.value)
  fetchExecAmountList(initProjId.value)
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
      <DateChoicer @set-date="setDate" />

      <TabSelect @tab-select="showTab" />

      <TableTitleRow excel :url="excelUrl" />

      <StatusByAccount v-if="compName === 'StatusByAccount'" :date="date" />
      <CashListByDate v-if="compName === 'CashListByDate'" :date="date" />
      <SummaryForBudget
        v-if="compName === 'SummaryForBudget'"
        :date="date"
        @patch-budget="patchBudget"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
