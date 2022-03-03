<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContChoicer
        ref="listControl"
        :contract="contract"
        @list-filtering="onContFiltering"
        @get-contract="getContract"
      />
      <CRow>
        <CCol lg="7">
          <PaymentList :contract="contract" :payment-list="paymentList" />

          <CAlert color="secondary" class="text-right">
            <CButton type="button" color="primary" :disabled="!contract">
              신규납부 등록
            </CButton>
          </CAlert>
        </CCol>
        <CCol lg="5">
          <OrdersBoard :contract="contract" :payment-list="paymentList" />
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/payments/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContChoicer from '@/views/payments/Register/components/ContChoicer.vue'
import PaymentList from '@/views/payments/Register/components/PaymentList.vue'
import PayForm from '@/views/payments/Register/components/PaymentForm.vue'
import OrdersBoard from '@/views/payments/Register/components/OrdersBoard.vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'PaymentsRegister',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContChoicer,
    PaymentList,
    PayForm,
    OrdersBoard,
  },
  created(this: any) {
    this.fetchTypeList(this.initProjId)
    this.fetchPayOrderList(this.initProjId)
    if (this.$route.query.contract) {
      this.$router.push({ name: '건별수납 관리' })
      this.getContract(this.$route.query.contract)
    }
    if (this.$route.query.payment) {
      this.$router.push({ name: '건별수납 관리' })
      this.getPayment(this.$route.query.payment)
    }
  },
  beforeRouteLeave(this: any) {
    this.$store.state.contract.contract = null
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
    ...mapState('contract', ['contract']),
    ...mapState('payment', ['paymentList']),
  },
  watch: {
    contract(this: any, newVal) {
      if (newVal) {
        const project = this.project.pk
        const order_group = newVal.order_group.pk
        const unit_type = newVal.unit_type.pk
        this.fetchPriceList({ project, order_group, unit_type })
        this.fetchDownPayList({ project, order_group, unit_type })
      } else {
        this.$store.state.payment.priceList = []
        this.$store.state.payment.downPayList = []
      }
    },
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchTypeList(target)
        this.fetchPayOrderList(target)
        this.proBankAccountList(target)
      } else {
        this.$store.state.contract.contract = null
        this.$store.state.contract.contractList = []
        this.$store.state.project.unitTypeList = []
        this.$store.state.payment.paymentList = []
        this.$store.state.payment.payOrderList = []
        this.$store.state.proCash.proBankAccountList = []
      }
    },
    onContFiltering(payload: any) {
      const project = this.project.pk
      this.fetchContractList({ ...{ project }, ...payload })
    },
    getContract(cont: number) {
      const project = this.project.pk
      this.fetchContract(cont)
      this.fetchPaymentList({ project, contract: cont, ordering: 'deal_date' })
    },
    getPayment(this: any, pk: string) {
      this.FETCH_PAYMENT_ID(Number(pk))
    },
    ...mapActions('project', ['fetchTypeList']),
    ...mapActions('payment', [
      'fetchPaymentList',
      'fetchPayOrderList',
      'fetchDownPayList',
      'fetchPriceList',
    ]),
    ...mapMutations('payment', ['FETCH_PAYMENT_ID']),
    ...mapActions('proCash', ['proBankAccountList']),
    ...mapActions('contract', ['fetchContractList', 'fetchContract']),
  },
})
</script>
