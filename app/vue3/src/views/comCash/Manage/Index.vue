<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="onSelectAdd"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddCash @on-create="onCreate" />
      <TableTitleRow title="본사 입출금 관리" color="indigo" excel disabled />
      <CashesList
        :company="company"
        @page-select="pageSelect"
        @on-update="onUpdate"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/comCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/comCash/Manage/components/ListController.vue'
import AddCash from '@/views/comCash/Manage/components/AddCash.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import CashesList from '@/views/comCash/Manage/components/CashesList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ComCashManage',
  components: {
    ContentHeader,
    ContentBody,
    ListController,
    AddCash,
    TableTitleRow,
    CashesList,
  },
  mixins: [HeaderMixin],
  data() {
    return {
      dataFilter: {
        page: 1,
        from_date: '',
        to_date: '',
        sort: '',
        account_d1: '',
        account_d2: '',
        account_d3: '',
        bank_account: '',
        search: '',
      },
    }
  },
  created() {
    this.fetchAccSortList()
    this.fetchAllAccD1List()
    this.fetchAllAccD2List()
    this.fetchAllAccD3List()
    this.fetchFormAccD1List()
    this.fetchFormAccD2List()
    this.fetchFormAccD3List()
    this.fetchComBankAccList(this.initComId)
    this.fetchCashBookList({ company: this.initComId })
  },
  computed: {
    ...mapState('settings', ['company']),
    ...mapGetters('accounts', ['initComId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchCompany(target)
        this.fetchComBankAccList(target)
        this.fetchCashBookList({ company: target })
      } else {
        this.$store.state.settings.company = null
        this.$store.state.comCash.comBankList = []
        this.$store.state.comCash.cashBookList = []
        this.$store.state.comCash.cashBookCount = 0
      }
    },
    pageSelect(this: any, page: number) {
      this.dataFilter.page = page
      this.$refs.listControl.listFiltering(page)
    },
    listFiltering(payload: any) {
      this.dataFilter = payload
      const company = this.company.pk
      const sort = payload.sort ? payload.sort : ''
      const d1 = payload.account_d1 ? payload.account_d1 : ''
      const d2 = payload.account_d2 ? payload.account_d2 : ''
      this.fetchFormAccD1List({ sort })
      this.fetchFormAccD2List({ sort, d1 })
      this.fetchFormAccD3List({ sort, d1, d2 })
      this.fetchCashBookList({ ...{ company }, ...payload })
    },
    onCreate(payload: any) {
      payload.company = this.company.pk
      if (payload.sort === '3' && payload.bank_account_to) {
        const { bank_account_to, income, ...outData } = payload
        this.createCashBook(outData)
        const { bank_account, outlay, ...incData } = outData
        this.createCashBook({
          ...{ bank_account: bank_account_to, income },
          ...incData,
        })
      } else this.createCashBook(payload)
    },
    onUpdate(payload: any) {
      this.updateCashBook({ ...{ filters: this.dataFilter }, ...payload })
    },
    onDelete(payload: any) {
      this.deleteCashBook({ ...{ filters: this.dataFilter }, ...payload })
    },
    ...mapActions('settings', ['fetchCompany']),
    ...mapActions('comCash', [
      'fetchAccSortList',
      'fetchAllAccD1List',
      'fetchAllAccD2List',
      'fetchAllAccD3List',
      'fetchFormAccD1List',
      'fetchFormAccD2List',
      'fetchFormAccD3List',
      'fetchComBankAccList',
      'fetchCashBookList',
      'createCashBook',
      'updateCashBook',
      'deleteCashBook',
    ]),
  },
})
</script>
