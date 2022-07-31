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

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/proCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/proCash/Status/components/DateChoicer.vue'
import TabSelect from '@/views/proCash/Status/components/TabSelect.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import StatusByAccount from '@/views/proCash/Status/components/StatusByAccount.vue'
import CashListByDate from '@/views/proCash/Status/components/CashListByDate.vue'
import SummaryForBudget from '@/views/proCash/Status/components/SummaryForBudget.vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

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
  mixins: [HeaderMixin],
  data() {
    return {
      compName: 'StatusByAccount',
      date: new Date(),
    }
  },
  created(this: any) {
    this.fetchProAllAccD1List()
    this.fetchProAllAccD2List()
    this.fetchProBankAccList(this.initProjId)
    this.fetchBalanceByAccList({ project: this.initProjId })
    this.fetchDateCashBookList({
      project: this.initProjId,
      date: this.dateFormat(this.date),
    })
    this.fetchProjectBudgetList(this.initProjId)
    this.fetchExecAmountList({ project: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchProBankAccList(target)
        this.fetchBalanceByAccList({ project: target })
        this.fetchDateCashBookList({
          project: target,
          date: this.dateFormat(this.date),
        })
        this.fetchProjectBudgetList(target)
        this.fetchExecAmountList({ project: target })
      } else {
        this.FETCH_P_BANK_ACCOUNT_LIST([])
        this.FETCH_BALANCE_BY_ACC_LIST([])
        this.FETCH_P_DATE_CASHBOOK([])
        this.FETCH_P_BUDGET_LIST([])
        this.FETCH_EXEC_AMOUNT_LIST([])
      }
    },
    showTab(num: number) {
      if (num === 1) this.compName = 'StatusByAccount'
      else if (num === 2) this.compName = 'CashListByDate'
      else if (num === 3) this.compName = 'SummaryForBudget'
    },
    setDate(this: any, date: string) {
      this.date = date
      const project = this.project.pk
      this.fetchBalanceByAccList({ project, date: this.dateFormat(date) })
      this.fetchDateCashBookList({ project, date: this.dateFormat(date) })
      this.fetchProjectBudgetList(project)
      this.fetchExecAmountList({ project, date: this.dateFormat(date) })
    },
    ...mapActions('proCash', [
      'fetchProAllAccD1List',
      'fetchProAllAccD2List',
      'fetchProBankAccList',
      'fetchBalanceByAccList',
      'fetchDateCashBookList',
      'fetchProjectBudgetList',
      'fetchExecAmountList',
    ]),
    ...mapMutations('proCash', [
      'FETCH_P_BANK_ACCOUNT_LIST',
      'FETCH_BALANCE_BY_ACC_LIST',
      'FETCH_P_DATE_CASHBOOK',
      'FETCH_P_BUDGET_LIST',
      'FETCH_EXEC_AMOUNT_LIST',
    ]),
  },
})
</script>
