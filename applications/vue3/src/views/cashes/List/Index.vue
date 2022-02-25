<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="onSelectAdd"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <ListController
        ref="listControl"
        @d1-select="accountD1Select"
        @d2-select="accountD2Select"
        @payment-filtering="onPayFiltering"
      />
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
import HeaderMixin from '@/views/cashes/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/cashes/List/components/ListController.vue'
import CashesList from '@/views/cashes/List/components/CashesList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'CashesIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ListController,
    CashesList,
  },
  created() {
    this.fetchAccountD1List()
    this.fetchAccountD2List()
    this.fetchAccountD3List()
    this.fetchCompanyBankAccountList(this.initProjId)
    this.fetchCashBookList({ company: this.initComId })
  },
  computed: {
    ...mapState('settings', ['company']),
    ...mapGetters('accounts', ['initComId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchProjectBankAccountList(target)
        this.fetchProjectCashList({ company: target })
      } else {
        this.$store.state.payment.proBankAccountList = []
        this.$store.state.payment.proCashBookList = []
        this.$store.state.payment.proCashesCount = 0
      }
    },
    accountD1Select(d1: number | string) {
      this.fetchAccountD2List(d1)
    },
    accountD2Select(d2: number | string) {
      this.fetchAccountD3List(d2)
    },
    pageSelect(this: any, page: number) {
      this.$refs.listControl.listFiltering(page)
    },
    onPayFiltering(payload: any) {
      const project = 1
      this.fetchCashBookList({ ...{ project }, ...payload })
    },
    onUpdate(payload: any) {
      console.log(payload)
    },
    onDelete(pk: number) {
      alert(pk)
    },
    ...mapActions('comCash', [
      'fetchAccountD1List',
      'fetchAccountD2List',
      'fetchAccountD3List',
      'fetchCompanyBankAccountList',
      'fetchCashBookList',
    ]),
  },
})
</script>
