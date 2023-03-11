<script lang="ts" setup>
import { computed, ref, onMounted, provide } from 'vue'
import { pageTitle, navMenu } from '@/views/payments/_menu/headermixin'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { PaymentFilter, usePayment } from '@/store/pinia/payment'
import { CashBookFilter, useProCash } from '@/store/pinia/proCash'
import { onBeforeRouteLeave } from 'vue-router'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PaymentSummary from '@/views/payments/List/components/PaymentSummary.vue'
import ListController from '@/views/payments/List/components/ListController.vue'
import PaymentList from '@/views/payments/List/components/PaymentList.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import { ProjectCashBook } from '@/store/types/proCash'

const listControl = ref()
let dataFilter = ref<PaymentFilter>({
  page: 1,
  from_date: '',
  to_date: '',
  order_group: '',
  unit_type: '',
  pay_order: '',
  pay_account: '',
  no_contract: false,
  search: '',
})

const projStore = useProject()
const initProjId = computed(() => projStore.initProjId)
const project = computed(() => projStore.project?.pk || initProjId.value)
const fetchIncBudgetList = (proj: number) => projStore.fetchIncBudgetList(proj)

const contStore = useContract()
const fetchOrderGroupList = (projId: number) =>
  contStore.fetchOrderGroupList(projId)
const fetchContSummaryList = (projId: number) =>
  contStore.fetchContSummaryList(projId)

const proDataStore = useProjectData()
const fetchTypeList = (projId: number) => proDataStore.fetchTypeList(projId)

const paymentStore = usePayment()
const fetchPaySumList = (projId: number) => paymentStore.fetchPaySumList(projId)
const fetchContNumList = (projId: number) =>
  paymentStore.fetchContNumList(projId)
const fetchPayOrderList = (projId: number) =>
  paymentStore.fetchPayOrderList(projId)
const fetchPaymentList = (payload: PaymentFilter) =>
  paymentStore.fetchPaymentList(payload)

const proCashStore = useProCash()
const fetchProBankAccList = (projId: number) =>
  proCashStore.fetchProBankAccList(projId)
const patchPrCashBook = (
  payload: ProjectCashBook & { filters: CashBookFilter },
) => proCashStore.patchPrCashBook(payload)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchOrderGroupList(target)
    fetchTypeList(target)
    fetchIncBudgetList(target)
    fetchContSummaryList(target)
    fetchPaySumList(target)
    fetchContNumList(target)
    fetchPaymentList({ project: target })
    fetchPayOrderList(target)
    fetchProBankAccList(target)
  } else {
    contStore.orderGroupList = []
    proDataStore.unitTypeList = []
    proCashStore.proBankAccountList = []
    projStore.proIncBudgetList = []
    contStore.contSummaryList = []
    paymentStore.paySumList = []
    paymentStore.contNumList = []
    paymentStore.paymentList = []
    paymentStore.payOrderList = []
    paymentStore.paymentsCount = 0
  }
}

const listFiltering = (payload: PaymentFilter) => {
  dataFilter.value = payload
  payload.project = project.value
  fetchPaymentList(payload)
}

const payMatch = (payload: ProjectCashBook) =>
  patchPrCashBook({ ...payload, filters: {} })

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  listControl.value.listFiltering(page)
}

const excelUrl = computed(() => {
  let url = project.value ? `/excel/payments/?project=${project.value}` : ''
  if (dataFilter.value.from_date) url += `&sd=${dataFilter.value.from_date}`
  if (dataFilter.value.to_date) url += `&ed=${dataFilter.value.to_date}`
  if (dataFilter.value.order_group) url += `&og=${dataFilter.value.order_group}`
  if (dataFilter.value.unit_type) url += `&ut=${dataFilter.value.unit_type}`
  if (dataFilter.value.pay_order) url += `&ipo=${dataFilter.value.pay_order}`
  if (dataFilter.value.pay_account) url += `&ba=${dataFilter.value.pay_account}`
  if (dataFilter.value.no_contract) url += `&up=on`
  if (dataFilter.value.search) url += `&q=${dataFilter.value.search}`
  return url
})

onMounted(() => {
  fetchOrderGroupList(project.value)
  fetchTypeList(project.value)
  fetchIncBudgetList(project.value)
  fetchContSummaryList(project.value)
  fetchPaySumList(project.value)
  fetchContNumList(project.value)
  fetchPayOrderList(project.value)
  fetchPaymentList({ project: project.value })
  fetchProBankAccList(project.value)
})

onBeforeRouteLeave(() => {
  paymentStore.paymentList = []
  paymentStore.paymentsCount = 0
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
        @pay-match="payMatch"
        @page-select="pageSelect"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
