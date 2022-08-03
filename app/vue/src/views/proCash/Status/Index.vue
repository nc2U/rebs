<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { pageTitle, navMenu } from '@/views/proCash/_menu/headermixin'
import { dateFormat } from '@/utils/baseMixins'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/proCash/Status/components/DateChoicer.vue'
import TabSelect from '@/views/proCash/Status/components/TabSelect.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import StatusByAccount from '@/views/proCash/Status/components/StatusByAccount.vue'
import CashListByDate from '@/views/proCash/Status/components/CashListByDate.vue'
import SummaryForBudget from '@/views/proCash/Status/components/SummaryForBudget.vue'

export default defineComponent({
  name: 'ProjectCashStatus',
  components: {
    ContentHeader,
    ContentBody,
    DateChoicer,
    TabSelect,
    TableTitleRow,
    StatusByAccount,
    CashListByDate,
    SummaryForBudget,
  },
  setup() {
    const store = useStore()

    const date = ref(new Date())
    const compName = ref('StatusByAccount')

    const project = computed(() => store.state.project.project)
    const initProjId = computed(() => store.getters['accounts/initProjId'])

    const fetchProAllAccD1List = () =>
      store.dispatch('proCash/fetchProAllAccD1List')
    const fetchProAllAccD2List = () =>
      store.dispatch('proCash/fetchProAllAccD2List')
    const fetchProBankAccList = (proj: number) =>
      store.dispatch('proCash/fetchProBankAccList', proj)
    const fetchBalanceByAccList = (proj: { project: number }) =>
      store.dispatch('proCash/fetchBalanceByAccList', proj)

    const fetchDateCashBookList = (payload: any) =>
      store.dispatch('proCash/fetchDateCashBookList', payload)
    const fetchProjectBudgetList = (proj: number) =>
      store.dispatch('proCash/fetchProjectBudgetList', proj)
    const fetchExecAmountList = (proj: { project: number }) =>
      store.dispatch('proCash/fetchExecAmountList', proj)

    const updateState = (payload: any) =>
      store.commit('proCash/updateState', payload)

    const onSelectAdd = (target: any) => {
      if (target !== '') {
        fetchProBankAccList(target)
        fetchBalanceByAccList({ project: target })
        fetchDateCashBookList({
          project: target,
          date: dateFormat(date.value),
        })
        fetchProjectBudgetList(target)
        fetchExecAmountList({ project: target })
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
      fetchBalanceByAccList({ project: project.value })
      fetchDateCashBookList({ project: project.value, date: dateFormat(dt) })
      fetchProjectBudgetList(project.value)
      fetchExecAmountList({ project: project.value })
    }

    onMounted(() => {
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

    return {
      date,
      compName,
      pageTitle,
      navMenu,
      onSelectAdd,
      showTab,
      setDate,
    }
  },
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

      <component :is="compName" :date="date" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
