<script lang="ts" setup>
import { computed, ref, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/payments/_menu/headermixin'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { usePayment } from '@/store/pinia/payment'
import { CashBookFilter, useProCash } from '@/store/pinia/proCash'
import { ProjectCashBook } from '@/store/types/proCash'
import { onBeforeRouteLeave } from 'vue-router'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PaymentSummary from '@/views/payments/List/components/PaymentSummary.vue'
import ListController from '@/views/payments/List/components/ListController.vue'
import PaymentList from '@/views/payments/List/components/PaymentList.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'

const listControl = ref()
let dataFilter = ref<CashBookFilter>({
  page: 1,
  from_date: '',
  to_date: '',
  pay_order: '',
  pay_account: '',
  no_contract: false,
  search: '',
})

const projectStore = useProject()
const project = computed(() => projectStore.project)
const initProjId = computed(() => projectStore.initProjId)

const excelUrl = computed(() => {
  let url = project.value ? `/excel/payments/?project=${project.value.pk}` : ''
  if (dataFilter.value.from_date) url += `&sd=${dataFilter.value.from_date}`
  if (dataFilter.value.to_date) url += `&ed=${dataFilter.value.to_date}`
  if (dataFilter.value.pay_order) url += `&ipo=${dataFilter.value.pay_order}`
  if (dataFilter.value.pay_account) url += `&ba=${dataFilter.value.pay_account}`
  if (dataFilter.value.no_contract) url += `&up=on`
  if (dataFilter.value.search) url += `&q=${dataFilter.value.search}`
  return url
})

const projectDataStore = useProjectData()
const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)

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
const patchPrCashBook = (payload: ProjectCashBook) =>
  proCashStore.patchPrCashBook(payload)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchTypeList(target)
    fetchPaySumList(target)
    fetchContNumList(target)
    fetchPaymentList({ project: target })
    fetchPayOrderList(target)
    fetchProBankAccList(target)
  } else {
    projectDataStore.unitTypeList = []
    proCashStore.proBankAccountList = []
    paymentStore.paySumList = []
    paymentStore.contNumList = []
    paymentStore.paymentList = []
    paymentStore.payOrderList = []
    paymentStore.paymentsCount = 0
  }
}

const listFiltering = (payload: CashBookFilter) => {
  dataFilter.value = payload
  payload.project = project.value?.pk || initProjId.value
  fetchPaymentList(payload)
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  listControl.value.listFiltering(page)
}

const onUpdate = (payload: ProjectCashBook) => {
  alert('a')
  console.log(payload)
}

const onPatch = (payload: ProjectCashBook) => patchPrCashBook(payload)

const onDelete = (pk: number) => alert(pk)

onMounted(() => {
  fetchTypeList(initProjId.value)
  fetchPaySumList(initProjId.value)
  fetchContNumList(initProjId.value)
  fetchPayOrderList(initProjId.value)
  fetchPaymentList({ project: initProjId.value })
  fetchProBankAccList(initProjId.value)
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
        @page-select="pageSelect"
        @on-update="onUpdate"
        @on-patch="onPatch"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
