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
          <PayList :contract="contract" :payment-list="paymentList"/>
          <PayForm/>
        </CCol>
        <CCol lg="5">
          <OrdersBoard :contract="contract" :payment-list="paymentList"/>
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import HeaderMixin from '@/views/payments/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContChoicer from '@/views/payments/Register/components/ContChoicer.vue'
import PayList from '@/views/payments/Register/components/PayList.vue'
import PayForm from '@/views/payments/Register/components/PayForm.vue'
import OrdersBoard from '@/views/payments/Register/components/OrdersBoard.vue'
import {mapActions, mapGetters, mapState} from 'vuex'

export default defineComponent({
  name: 'PaymentsRegister',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContChoicer,
    PayList,
    PayForm,
    OrdersBoard,
  },
  created(this: any) {
    this.fetchTypeList(this.initProjId)
    this.fetchPayOrderList(this.initProjId)
    if (this.$route.query.contract) {
      this.$router.push({name: '건별수납 관리'})
      this.getContract(this.$route.query.contract)
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
        this.fetchPriceList({project, order_group, unit_type})
        this.fetchDownPayList({project, order_group, unit_type})
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
      } else {
        this.$store.state.contract.contract = null
        this.$store.state.contract.contractList = []
        this.$store.state.project.unitTypeList = []
        this.$store.state.payment.paymentList = []
        this.$store.state.payment.payOrderList = []
      }
    },
    onContFiltering(payload: any) {
      const project = this.project.pk
      this.fetchContractList({...{project}, ...payload})
    },
    getContract(cont: number) {
      const project = this.project.pk
      this.fetchContract(cont)
      this.fetchPaymentList({project, contract: cont})
    },
    ...mapActions('project', ['fetchTypeList']),
    ...mapActions('payment', [
      'fetchPaymentList',
      'fetchPayOrderList',
      'fetchDownPayList',
      'fetchPriceList',
    ]),
    ...mapActions('contract', ['fetchContractList', 'fetchContract']),
  },
})
</script>
