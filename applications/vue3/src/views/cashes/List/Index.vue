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
    this.fetchProAccountD1List()
    this.fetchProAccountD2List()
    this.fetchProjectBankAccountList(this.initProjId)
    this.fetchProjectCashList({ project: this.initProjId })
  },
  computed: {
    ...mapState('settings', ['company']),
    ...mapGetters('accounts', ['initComId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchProjectBankAccountList(target)
        this.fetchProjectCashList({ project: target })
      } else {
        this.$store.state.payment.proBankAccountList = []
        this.$store.state.payment.proCashBookList = []
        this.$store.state.payment.proCashesCount = 0
      }
    },
    accountD1Select(d1: number | string) {
      this.fetchProAccountD2List(d1)
    },
    pageSelect(this: any, page: number) {
      this.$refs.listControl.listFiltering(page)
    },
    onPayFiltering(payload: any) {
      const project = 1
      this.fetchProjectCashList({ ...{ project }, ...payload })
    },
    onUpdate(payload: any) {
      console.log(payload)
    },
    onDelete(pk: number) {
      alert(pk)
    },
    ...mapActions('proCash', [
      'fetchProAccountD1List',
      'fetchProAccountD2List',
      'fetchProjectBankAccountList',
      'fetchProjectCashList',
    ]),
  },
})
</script>
