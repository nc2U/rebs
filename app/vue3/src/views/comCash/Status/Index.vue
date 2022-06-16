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
    this.fetchAllAccD1List()
    this.fetchAllAccD2List()
    this.fetchAllAccD3List()
    this.fetchComBankAccList(this.initComId)
    this.fetchComBalanceByAccList({ company: this.initComId })
    this.fetchDateCashBookList({
      company: this.initComId,
      date: this.dateFormat(this.date),
    })
  },
  computed: {
    ...mapState('settings', ['company']),
    ...mapGetters('accounts', ['initComId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchComBankAccList(target)
        this.fetchComBalanceByAccList({ company: target })
        this.fetchDateCashBookList({
          company: target,
          date: this.dateFormat(this.date),
        })
      } else {
        this.FETCH_COMPAY_BANK_LIST([])
        this.FETCH_BALANCE_BY_ACC_LIST([])
        this.FETCH_DATE_CASHBOOK([])
      }
    },
    showTab(num: number) {
      if (num === 1) this.compName = 'StatusByAccount'
      else if (num === 2) this.compName = 'CashListByDate'
    },
    setDate(this: any, date: string) {
      this.date = date
      const company = this.company.pk
      this.fetchComBalanceByAccList({ company, date: this.dateFormat(date) })
      this.fetchDateCashBookList({ company, date: this.dateFormat(date) })
    },
    ...mapActions('comCash', [
      'fetchAllAccD1List',
      'fetchAllAccD2List',
      'fetchAllAccD3List',
      'fetchComBankAccList',
      'fetchComBalanceByAccList',
      'fetchDateCashBookList',
    ]),
    ...mapMutations('comCash', [
      'FETCH_COMPAY_BANK_LIST',
      'FETCH_BALANCE_BY_ACC_LIST',
      'FETCH_DATE_CASHBOOK',
    ]),
  },
})
</script>
