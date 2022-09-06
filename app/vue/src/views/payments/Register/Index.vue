<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { useRouter, useRoute, onBeforeRouteLeave } from 'vue-router'
import { pageTitle, navMenu } from '@/views/payments/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContChoicer from '@/views/payments/Register/components/ContChoicer.vue'
import PaymentListAll from '@/views/payments/Register/components/PaymentListAll.vue'
import OrdersBoard from '@/views/payments/Register/components/OrdersBoard.vue'
import CreateButton from '@/views/payments/Register/components/CreateButton.vue'

const paymentId = ref<any>('')

const store = useStore()
const projectStore = useProject()

const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const contract = computed(() => store.state.contract.contract)
const AllPaymentList = computed(() => store.state.payment.AllPaymentList)

const fetchTypeList = (projId: number) =>
  store.dispatch('project/fetchTypeList', projId)
const fetchAllPaymentList = (payload: any) =>
  store.dispatch('payment/fetchAllPaymentList', payload)
const fetchPayOrderList = (projId: number) =>
  store.dispatch('payment/fetchPayOrderList', projId)
const fetchDownPayList = (payload: any) =>
  store.dispatch('payment/fetchDownPayList', payload)
const fetchPriceList = (payload: any) =>
  store.dispatch('payment/fetchPriceList', payload)

const fetchProBankAccList = (projId: number) =>
  store.dispatch('proCash/fetchProBankAccList', projId)
const createPrCashBook = (payload: any) =>
  store.dispatch('proCash/createPrCashBook', payload)
const updatePrCashBook = (payload: any) =>
  store.dispatch('proCash/updatePrCashBook', payload)
const deletePrCashBook = (payload: any) =>
  store.dispatch('proCash/deletePrCashBook', payload)

const fetchContractList = (payload: any) =>
  store.dispatch('contract/fetchContractList', payload)
const fetchContract = (cont: any) =>
  store.dispatch('contract/fetchContract', cont)

const route = useRoute()
const router = useRouter()

onBeforeMount(() => {
  if (route.query.contract) {
    router.replace({
      name: '건별수납 관리',
      query: { contract: route.query.contract },
    })
    getContract(route.query.contract)
  }
  if (route.query.payment) paymentId.value = route.query.payment

  fetchTypeList(initProjId.value)
  fetchPayOrderList(initProjId.value)
  fetchProBankAccList(initProjId.value)
})

watch(contract, newVal => {
  if (newVal) {
    const order_group = newVal.order_group.pk
    const unit_type = newVal.unit_type.pk
    fetchPriceList({ project: project.value, order_group, unit_type })
    fetchDownPayList({ project: project.value, order_group, unit_type })
    fetchAllPaymentList({
      project: project.value,
      contract: newVal.pk,
      ordering: 'deal_date',
    })
  } else {
    store.commit('payment/updateState', {
      priceList: [],
      downPayList: [],
      AllPaymentList: [],
    })
  }
})

const onSelectAdd = (target: any) => {
  router.push({ name: '건별수납 관리' })
  store.commit('contract/updateState', { contract: null, contractList: [] })
  store.commit('project/updateState', { unitTypeList: [] })
  store.commit('payment/updateState', {
    AllPaymentList: [],
    payOrderList: [],
  })
  store.commit('proCash/updateState', { proBankAccountList: [] })
  if (target !== '') {
    fetchTypeList(target)
    fetchPayOrderList(target)
    fetchProBankAccList(target)
  }
}

const onContFiltering = (payload: any) =>
  fetchContractList({ ...{ project: project.value }, ...payload })

const getContract = (cont: any) => {
  router.replace({
    name: '건별수납 관리',
    query: { contract: cont },
  })
  fetchContract(cont)
}

const onCreate = (payload: any) => {
  payload.project = project.value
  createPrCashBook(payload)
}
const onUpdate = (payload: any) => {
  payload.project = project.value
  updatePrCashBook(payload)
}
const onDelete = (pk: number) =>
  deletePrCashBook({ project: project.value, pk, contract: contract.value.pk })

onBeforeRouteLeave(() => {
  store.commit('contract/updateState', { contract: null })
})
</script>

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
        :project="project"
        :contract="contract"
        @list-filtering="onContFiltering"
        @get-contract="getContract"
      />
      <CRow>
        <CCol lg="7">
          <PaymentListAll
            :contract="contract"
            :payment-id="paymentId"
            :payment-list="AllPaymentList"
            @on-update="onUpdate"
            @on-delete="onDelete"
          />

          <CreateButton :contract="contract" @on-create="onCreate" />
        </CCol>
        <CCol lg="5">
          <OrdersBoard :contract="contract" :payment-list="AllPaymentList" />
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
