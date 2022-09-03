<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
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

const store = useStore()
const projectStore = useProject()

const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const fetchProAllAccD1List = () =>
  store.dispatch('proCash/fetchProAllAccD1List')
const fetchProAllAccD2List = () =>
  store.dispatch('proCash/fetchProAllAccD2List')
const fetchProBankAccList = (proj: number) =>
  store.dispatch('proCash/fetchProBankAccList', proj)

const fetchBalanceByAccList = (proj: { project: number; date?: string }) =>
  store.dispatch('proCash/fetchBalanceByAccList', proj)
const fetchDateCashBookList = (payload: any) =>
  store.dispatch('proCash/fetchDateCashBookList', payload)
const fetchProjectBudgetList = (proj: number) =>
  store.dispatch('proCash/fetchProjectBudgetList', proj)
const fetchExecAmountList = (proj: { project: number; date?: string }) =>
  store.dispatch('proCash/fetchExecAmountList', proj)

const updateState = (payload: any) =>
  store.commit('proCash/updateState', payload)

const onSelectAdd = (target: any) => {
  if (target !== '') {
    fetchProBankAccList(target)
    fetchBalanceByAccList({ project: target, date: dateFormat(date.value) })
    fetchDateCashBookList({
      project: target,
      date: dateFormat(date.value),
    })
    fetchProjectBudgetList(target)
    fetchExecAmountList({ project: target, date: dateFormat(date.value) })
  } else {
    updateState({
      proBankAccountList: [],
      balanceByAccList: [],
      proDateCashBook: [],
      proBudgetList: [],
      execAmountList: [],
    })
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
  fetchExecAmountList({ project: project.value, date: dateFormat(dt) })
}

onBeforeMount(() => {
  fetchProAllAccD1List()
  fetchProAllAccD2List()
  fetchProBankAccList(initProjId.value)
  fetchBalanceByAccList({ project: initProjId.value })
  fetchDateCashBookList({
    project: initProjId.value,
    date: dateFormat(date.value),
  })
  fetchProjectBudgetList(initProjId.value)
  fetchExecAmountList({ project: initProjId.value })
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

      <TableTitleRow excel disabled />

      <StatusByAccount v-if="compName === 'StatusByAccount'" :date="date" />
      <CashListByDate v-if="compName === 'CashListByDate'" :date="date" />
      <SummaryForBudget v-if="compName === 'SummaryForBudget'" :date="date" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
