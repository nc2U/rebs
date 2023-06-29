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
const direct = ref('0')
const compName = ref('StatusByAccount')

const projStore = useProject()
const project = computed(() => projStore.project?.pk || projStore.initProjId)

const fetchStatusOutBudgetList = (proj: number) =>
  projStore.fetchStatusOutBudgetList(proj)
const patchStatusOutBudgetList = (proj: number, pk: number, budget: number) =>
  projStore.patchStatusOutBudgetList(proj, pk, budget)
const fetchExecAmountList = (project: number, date?: string) =>
  projStore.fetchExecAmountList(project, date)

const pCashStore = useProCash()
const fetchProAllAccD2List = () => pCashStore.fetchProAllAccD2List()
const fetchProAllAccD3List = () => pCashStore.fetchProAllAccD3List()
const fetchProBankAccList = (proj: number) =>
  pCashStore.fetchProBankAccList(proj)

const fetchBalanceByAccList = (payload: {
  project: number
  direct?: string
  date?: string
}) => pCashStore.fetchBalanceByAccList(payload)
const fetchDateCashBookList = (payload: { project: number; date: string }) =>
  pCashStore.fetchDateCashBookList(payload)

const excelUrl = computed(() => {
  const comp = compName.value
  const pj = project.value
  const dr = direct.value
  const dt = dateFormat(date.value)
  let url = ''
  if (comp === 'StatusByAccount')
    url = `/excel/p-balance/?project=${pj}&date=${dt}&bank_account__directpay=${dr}`
  else if (comp === 'CashListByDate')
    url = `/excel/p-daily-cash/?project=${pj}&date=${dt}`
  else if (comp === 'SummaryForBudget')
    url = `/excel/p-budget/?project=${pj}&date=${dt}`
  return `${url}`
})

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchStatusOutBudgetList(target)
    fetchExecAmountList(target, dateFormat(date.value))
    fetchProBankAccList(target)
    fetchBalanceByAccList({ project: target, date: dateFormat(date.value) })
    fetchDateCashBookList({
      project: target,
      date: dateFormat(date.value),
    })
  } else {
    projStore.statusOutBudgetList = []
    projStore.execAmountList = []
    pCashStore.proBankAccountList = []
    pCashStore.balanceByAccList = []
    pCashStore.proDateCashBook = []
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
  if (project.value) {
    fetchStatusOutBudgetList(project.value)
    fetchExecAmountList(project.value, dateFormat(dt))
    fetchBalanceByAccList({ project: project.value, date: dateFormat(dt) })
    fetchDateCashBookList({ project: project.value, date: dateFormat(dt) })
  }
}

const patchBudget = (pk: number, budget: number) => {
  if (project.value) patchStatusOutBudgetList(project.value, pk, budget)
}

const directBalance = (val: boolean) => {
  direct.value = val ? 'i' : '0'
  if (project.value)
    fetchBalanceByAccList({
      project: project.value,
      direct: direct.value,
      date: dateFormat(date.value),
    })
}

onBeforeMount(() => {
  fetchProAllAccD2List()
  fetchProAllAccD3List()

  const projectPk = project.value
  fetchExecAmountList(projectPk)
  fetchStatusOutBudgetList(projectPk)
  fetchProBankAccList(projectPk)
  fetchBalanceByAccList({
    project: projectPk,
    date: dateFormat(date.value),
  })
  fetchDateCashBookList({
    project: projectPk,
    date: dateFormat(date.value),
  })
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

      <TableTitleRow excel :url="excelUrl" :disabled="!project" />

      <StatusByAccount
        v-if="compName === 'StatusByAccount'"
        :date="date"
        @direct-balance="directBalance"
      />
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
