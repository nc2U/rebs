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
import ListController from '@/views/comCash/List/components/ListController.vue'
import CashesList from '@/views/comCash/List/components/CashesList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'comCashIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ListController,
    CashesList,
  },
  data() {
    return {
      page: 1,
    }
  },
  created() {
    this.fetchAccSortList()
    this.fetchAccD1List()
    this.fetchAccD2List()
    this.fetchAccD3List()
    this.fetchAccountD1List()
    this.fetchAccountD2List()
    this.fetchAccountD3List()
    this.fetchCompanyBankAccountList(this.initComId)
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
        this.fetchCompanyBankAccountList(target)
        this.fetchCashBookList({ company: target })
      } else {
        this.$store.state.settings.company = null
        this.$store.state.comCash.comBankList = []
        this.$store.state.comCash.cashBookList = []
        this.$store.state.comCash.cashBookCount = 0
      }
    },
    pageSelect(this: any, page: number) {
      this.page = page
      this.$refs.listControl.listFiltering(page)
    },
    listFiltering(payload: any) {
      const company = this.company.pk
      const sort = payload.sort ? payload.sort : ''
      const d1 = payload.account_d1 ? payload.account_d1 : ''
      const d2 = payload.account_d2 ? payload.account_d2 : ''
      this.fetchAccountD1List({ sort })
      this.fetchAccountD2List({ sort, d1 })
      this.fetchAccountD3List({ sort, d1, d2 })
      this.fetchCashBookList({ ...{ company }, ...payload })
    },
    onUpdate(payload: any) {
      const page = this.page
      this.updateCashBook({ ...{ page }, ...payload })
    },
    onDelete(payload: any) {
      const page = this.page
      this.deleteCashBook({ ...{ page }, ...payload })
    },
    ...mapActions('settings', ['fetchCompany']),
    ...mapActions('comCash', [
      'fetchAccSortList',
      'fetchAccD1List',
      'fetchAccD2List',
      'fetchAccD3List',
      'fetchAccountD1List',
      'fetchAccountD2List',
      'fetchAccountD3List',
      'fetchCompanyBankAccountList',
      'fetchCashBookList',
      'updateCashBook',
      'deleteCashBook',
    ]),
  },
})
</script>
