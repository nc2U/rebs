<script lang="ts" setup>
import { computed, ref, onMounted, reactive } from 'vue'
import { useStore } from 'vuex'
import { onBeforeRouteLeave } from 'vue-router'
import { pageTitle, navMenu } from '@/views/payments/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PaymentSummary from '@/views/payments/List/components/PaymentSummary.vue'
import ListController from '@/views/payments/List/components/ListController.vue'
import PaymentList from '@/views/payments/List/components/PaymentList.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

const store = useStore()

const listControl = ref()
let dataFilter = reactive({
  page: 1,
  from_date: '',
  to_date: '',
  pay_order: '',
  pay_account: '',
  no_contract: false,
  search: '',
})

const project = computed(() => store.state.project.project)
const initProjId = computed(() => store.getters['accounts/initProjId'])

const fetchTypeList = (pj: number) =>
  store.dispatch('project/fetchTypeList', pj)
const fetchPaySumList = (pj: number) =>
  store.dispatch('payment/fetchPaySumList', pj)
const fetchContNumList = (pj: number) =>
  store.dispatch('payment/fetchContNumList', pj)
const fetchPayOrderList = (pj: number) =>
  store.dispatch('payment/fetchPayOrderList', pj)
const fetchPaymentList = (pj: { project: number }) =>
  store.dispatch('payment/fetchPaymentList', pj)
const fetchProBankAccList = (pj: number) =>
  store.dispatch('proCash/fetchProBankAccList', pj)
const patchPrCashBook = (payload: any) =>
  store.dispatch('proCash/patchPrCashBook', payload)

const projectUpdateState = (payload: any) =>
  store.commit('project/updateState', payload)
const paymentUpdateState = (payload: any) =>
  store.commit('payment/updateState', payload)
const proCashUpdateState = (payload: any) =>
  store.commit('proCash/updateState', payload)

onMounted(() => {
  fetchTypeList(initProjId.value)
  fetchPaySumList(initProjId.value)
  fetchContNumList(initProjId.value)
  fetchPayOrderList(initProjId.value)
  fetchPaymentList({ project: initProjId.value })
  fetchProBankAccList(initProjId.value)
})

const onSelectAdd = (target: any) => {
  if (target !== '') {
    fetchTypeList(target)
    fetchPaySumList(target)
    fetchContNumList(target)
    fetchPaymentList({ project: target })
    fetchPayOrderList(target)
    fetchProBankAccList(target)
  } else {
    projectUpdateState({ unitTypeList: [] })
    proCashUpdateState({ proBankAccountList: [] })
    paymentUpdateState({
      paySumList: [],
      contNumList: [],
      paymentList: [],
      payOrderList: [],
      paymentsCount: 0,
    })
  }
}

const pageSelect = (page: number) => {
  dataFilter.page = page
  listControl.value.listFiltering(page)
}

const listFiltering = (payload: any) => {
  dataFilter = payload
  fetchPaymentList({ ...{ project: project.value.pk }, ...payload })
}

const onUpdate = (payload: any) => {
  alert('a')
  console.log(payload)
}

const onPatch = (payload: any) => {
  patchPrCashBook(payload)
}

const onDelete = (pk: number) => {
  alert(pk)
}

onBeforeRouteLeave(() => {
  store.state.payment.paymentList = []
  store.state.payment.paymentsCount = 0
})
</script>

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
      <ListController ref="listControl" @payment-filtering="listFiltering" />
      <TableTitleRow excel :url="excelUrl" />
      <PaymentList
        :project="project"
        @page-select="pageSelect"
        @on-update="onUpdate"
        @on-patch="onPatch"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
