<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="onSelectAdd"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <DateChoicer @set-date="setDate" />

      <TabSelect @tab-select="showTab" />

      <CRow class="text-right mb-2">
        <CCol>Excel Export</CCol>
      </CRow>

      <component :is="compName" :date="date" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/comCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/comCash/Status/components/DateChoicer.vue'
import TabSelect from '@/views/comCash/Status/components/TabSelect.vue'
import StatusByAccount from '@/views/comCash/Status/components/StatusByAccount.vue'
import CashListByDate from '@/views/comCash/Status/components/CashListByDate.vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'CashesStatus',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    DateChoicer,
    TabSelect,
    StatusByAccount,
    CashListByDate,
  },
  data() {
    return {
      compName: 'StatusByAccount',
      date: new Date(),
    }
  },
  created(this: any) {
    // this.fetchProAllAccD1List()
    // this.fetchProAllAccD2List()
    // this.fetchProBankAccList(this.initProjId)
    // this.fetchBalanceByAccList({ project: this.initProjId })
    // this.fetchDateCashBookList({
    //   project: this.initProjId,
    //   date: this.dateFormat(this.date),
    // })
    // this.fetchProjectBudgetList(this.initProjId)
    // this.fetchExecAmountList({ project: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    // onSelectAdd(this: any, target: any) {
    //   if (target !== '') {
    //     // this.fetchProBankAccList(target)
    //     // this.fetchBalanceByAccList({ project: target })
    //     // this.fetchDateCashBookList({
    //     //   project: target,
    //     //   date: this.dateFormat(this.date),
    //     // })
    //     // this.fetchProjectBudgetList(target)
    //     // this.fetchExecAmountList({ project: target })
    //   } else {
    //     // this.FETCH_P_BANK_ACCOUNT_LIST([])
    //     // this.FETCH_BALANCE_BY_ACC_LIST([])
    //     // this.FETCH_P_DATE_CASHBOOK([])
    //     // this.FETCH_P_BUDGET_LIST([])
    //     // this.FETCH_EXEC_AMOUNT_LIST([])
    //   }
    // },
    showTab(num: number) {
      if (num === 1) this.compName = 'StatusByAccount'
      else if (num === 2) this.compName = 'CashListByDate'
    },
    setDate(this: any, date: string) {
      this.date = date
      const project = this.project.pk
      // this.fetchBalanceByAccList({ project, date: this.dateFormat(date) })
      // this.fetchDateCashBookList({ project, date: this.dateFormat(date) })
      // this.fetchProjectBudgetList(project)
      // this.fetchExecAmountList({ project, date: this.dateFormat(date) })
    },
    // ...mapActions('proCash', [
    //   'fetchProAllAccD1List',
    //   'fetchProAllAccD2List',
    //   'fetchProBankAccList',
    //   'fetchBalanceByAccList',
    //   'fetchDateCashBookList',
    //   'fetchProjectBudgetList',
    //   'fetchExecAmountList',
    // ]),
    // ...mapMutations('proCash', [
    //   'FETCH_P_BANK_ACCOUNT_LIST',
    //   'FETCH_BALANCE_BY_ACC_LIST',
    //   'FETCH_P_DATE_CASHBOOK',
    //   'FETCH_P_BUDGET_LIST',
    //   'FETCH_EXEC_AMOUNT_LIST',
    // ]),
  },
})
</script>
