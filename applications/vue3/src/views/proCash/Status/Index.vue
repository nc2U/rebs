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
import HeaderMixin from '@/views/proCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/proCash/Status/components/DateChoicer.vue'
import TabSelect from '@/views/proCash/Status/components/TabSelect.vue'
import StatusByAccount from '@/views/proCash/Status/components/StatusByAccount.vue'
import CashListByDate from '@/views/proCash/Status/components/CashListByDate.vue'
import SummaryForBudget from '@/views/proCash/Status/components/SummaryForBudget.vue'
import { mapActions, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectCashStatus',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    DateChoicer,
    TabSelect,
    StatusByAccount,
    CashListByDate,
    SummaryForBudget,
  },
  data() {
    return {
      compName: 'StatusByAccount',
      date: new Date(),
    }
  },
  created() {
    this.fetchBalanceByAccList()
  },
  computed: {
    ...mapState('project', ['project']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchBalanceByAccList()
      } else {
        this.FETCH_BALANCE_BY_ACC_LIST([])
      }
    },
    showTab(num: number) {
      if (num === 1) this.compName = 'StatusByAccount'
      else if (num === 2) this.compName = 'CashListByDate'
      else if (num === 3) this.compName = 'SummaryForBudget'
    },
    setDate(this: any, date: string) {
      this.date = date
      this.fetchBalanceByAccList(date)
    },
    ...mapActions('proCash', ['fetchBalanceByAccList']),
    ...mapMutations('proCash', ['FETCH_BALANCE_BY_ACC_LIST']),
  },
})
</script>
