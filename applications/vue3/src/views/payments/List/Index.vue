<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  >
    <PaymentSummary :project="project" />
  </ContentHeader>

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @payment-filtering="onPayFiltering" />
      <PaymentList
        :project="project"
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
import HeaderMixin from '@/views/payments/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PaymentSummary from '@/views/payments/List/components/PaymentSummary.vue'
import ListController from '@/views/payments/List/components/ListController.vue'
import PaymentList from '@/views/payments/List/components/PaymentList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'PaymentsList',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    PaymentSummary,
    ListController,
    PaymentList,
  },
  created() {
    this.fetchTypeList(this.initProjId)
    this.fetchPaymentList({ project: this.initProjId })
    this.fetchPayOrderList(this.initProjId)
    this.fetchProjectBankAccountList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchTypeList(target)
        this.fetchPaymentList({ project: target })
        this.fetchPayOrderList(target)
        this.fetchProjectBankAccountList(target)
      } else {
        this.$store.state.project.unitTypeList = []
        this.$store.state.cash.paymentList = []
        this.$store.state.cash.payOrderList = []
        this.$store.state.cash.pBankAccountList = []
      }
    },
    pageSelect(this: any, page: number) {
      this.$refs.listControl.listFiltering(page)
    },
    onPayFiltering(payload: any) {
      const project = this.project.pk
      this.fetchPaymentList({ ...{ project }, ...payload })
    },
    onUpdate(payload: any) {
      alert('a')
      console.log(payload)
    },
    onDelete(pk: number) {
      alert(pk)
    },
    ...mapActions('project', ['fetchTypeList']),
    ...mapActions('payment', [
      'fetchPayOrderList',
      'fetchPaymentList',
      'fetchProjectBankAccountList',
    ]),
  },
})
</script>
