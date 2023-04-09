<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { navMenu, pageTitle } from '@/views/payments/_menu/headermixin'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { usePayment } from '@/store/pinia/payment'
import { useProCash } from '@/store/pinia/proCash'
import { CashBookFilter, ProjectCashBook } from '@/store/types/proCash'
import { onBeforeRouteLeave } from 'vue-router'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PaymentSummary from '@/views/payments/List/components/PaymentSummary.vue'
import ListController from '@/views/payments/List/components/ListController.vue'
import PaymentList from '@/views/payments/List/components/PaymentList.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'

const listControl = ref()
let filterItems = ref<CashBookFilter>({
  page: 1,
  from_date: '',
  to_date: '',
  order_group: '',
  unit_type: '',
  pay_order: '',
  pay_account: '',
  no_contract: false,
  no_install: false,
  search: '',
})

const projStore = useProject()
const project = computed(() => projStore.project?.pk)
const initProjId = computed(() => projStore.initProjId)

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
const fetchPaymentList = (payload: CashBookFilter) =>
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

const listFiltering = (payload: CashBookFilter) => {
  filterItems.value = payload
  if (project.value) {
    payload.project = project.value
    fetchPaymentList(payload)
  }
}

const payMatch = (payload: ProjectCashBook) =>
  patchPrCashBook({ ...payload, filters: filterItems.value }) // const & payment 매칭

const pageSelect = (page: number) => {
  filterItems.value.page = page
  listControl.value.listFiltering(page)
}

const byPayment = computed(() => {
  let pUrl = project.value ? `/excel/payments/?project=${project.value}` : ''
  if (filterItems.value.from_date) pUrl += `&sd=${filterItems.value.from_date}`
  if (filterItems.value.to_date) pUrl += `&ed=${filterItems.value.to_date}`
  if (filterItems.value.order_group)
    pUrl += `&og=${filterItems.value.order_group}`
  if (filterItems.value.unit_type) pUrl += `&ut=${filterItems.value.unit_type}`
  if (filterItems.value.pay_order) pUrl += `&ipo=${filterItems.value.pay_order}`
  if (filterItems.value.pay_account)
    pUrl += `&ba=${filterItems.value.pay_account}`
  if (filterItems.value.no_contract) pUrl += `&nc=true`
  if (filterItems.value.no_install) pUrl += `&ni=true`
  if (filterItems.value.search) pUrl += `&q=${filterItems.value.search}`
  return pUrl
})

const byContract = computed(() =>
  project.value
    ? `/excel/paid-by-cont/?project=${project.value}&date=${filterItems.value.to_date}`
    : '',
)

const excelSelect = ref('1') // 다운로드할 파일 선택

const excelUrl = computed(() =>
  excelSelect.value === '1' ? byPayment.value : byContract.value,
)

onMounted(() => {
  if (initProjId.value) {
    fetchOrderGroupList(initProjId.value)
    fetchTypeList(initProjId.value)
    fetchIncBudgetList(initProjId.value)
    fetchContSummaryList(initProjId.value)
    fetchPaySumList(initProjId.value)
    fetchContNumList(initProjId.value)
    fetchPayOrderList(initProjId.value)
    fetchPaymentList({ project: initProjId.value })
    fetchProBankAccList(initProjId.value)
  }
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
      <ListController
        ref="listControl"
        :by-cont="excelSelect === '2'"
        @payment-filtering="listFiltering"
      />
      <TableTitleRow excel :url="excelUrl" :disabled="!project">
        <v-radio-group
          v-model="excelSelect"
          inline
          size="sm"
          density="compact"
          color="success"
          class="d-flex flex-row-reverse"
          style="font-size: 0.8em"
        >
          <v-radio label="수납건별" value="1" class="pr-3" />
          <v-radio label="계약자별" value="2" />
        </v-radio-group>
      </TableTitleRow>
      <PaymentList
        :page="filterItems.page"
        :project="project"
        @pay-match="payMatch"
        @page-select="pageSelect"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
