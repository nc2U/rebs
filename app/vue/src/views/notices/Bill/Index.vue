<script lang="ts" setup>
import { ref, reactive, computed, watch, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { useNotice } from '@/store/pinia/notice'
import { usePayment } from '@/store/pinia/payment'
import { useContract } from '@/store/pinia/contract'
import { dateFormat } from '@/utils/baseMixins'
import { pageTitle, navMenu } from '@/views/notices/_menu/headermixin'
import { SalesBillIssue } from '@/store/types/notice'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import SalesBillIssueForm from '@/views/notices/Bill/components/SalesBillIssueForm.vue'
import ListController from '@/views/notices/Bill/components/ListController.vue'
import DownloadButton from '@/views/notices/Bill/components/DownloadButton.vue'
import ContractList from '@/views/notices/Bill/components/ContractList.vue'

const listControl = ref()
const contractList = ref()
defineExpose({ listControl, contractList })

const ctor_ids = ref([])
const print_data = reactive({
  is_bill_issue: false,
  project: null as null | number,
  pub_date: dateFormat(new Date()),
})

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const noticeStore = useNotice()
const billIssue = computed(() => noticeStore.billIssue)

const fetchSalesBillIssue = (projId: number) =>
  noticeStore.fetchSalesBillIssue(projId)
const createSalesBillIssue = (payload: SalesBillIssue) =>
  noticeStore.createSalesBillIssue(payload)
const patchSalesBillIssue = (payload: SalesBillIssue) =>
  noticeStore.patchSalesBillIssue(payload)

const paymentStore = usePayment()
const payOrder = computed(() => paymentStore.payOrder)

const payOrderTime = computed(() =>
  payOrder.value ? payOrder.value.pay_time : null,
)
const payOrderName = computed(() =>
  payOrder.value ? payOrder.value.__str__ : '',
)

const fetchPayOrder = (payload: any) => paymentStore.fetchPayOrder(payload)
const patchPayOrder = (payload: any) => paymentStore.patchPayOrder(payload)
const fetchPayOrderList = (projId: number) =>
  paymentStore.fetchPayOrderList(projId)

const projectDataStore = useProjectData()
const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)
const fetchBuildingList = (projId: number) =>
  projectDataStore.fetchBuildingList(projId)

const contractStore = useContract()
const fetchOrderGroupList = (projId: number) =>
  contractStore.fetchOrderGroupList(projId)
const fetchContractList = (payload: { project: number; ordering: string }) =>
  contractStore.fetchContractList(payload)
const fetchSalePriceList = (payload: { project: number }) =>
  contractStore.fetchSalePriceList(payload)
const fetchDownPayList = (payload: { project: number }) =>
  contractStore.fetchDownPayList(payload)

onBeforeMount(() => {
  fetchSalesBillIssue(initProjId.value)
  fetchPayOrderList(initProjId.value)
  fetchOrderGroupList(initProjId.value)
  fetchTypeList(initProjId.value)
  fetchBuildingList(initProjId.value)
  fetchContractList({
    project: initProjId.value,
    ordering: 'contractor__name',
  })
  fetchSalePriceList({ project: initProjId.value })
  fetchDownPayList({ project: initProjId.value })
})

watch(project, val => {
  if (val) {
    fetchSalesBillIssue(val)
    print_data.project = val
  }
})

watch(billIssue, val => {
  if (val) {
    print_data.is_bill_issue = !!val
    fetchPayOrder(val.now_payment_order)
  }
})

const onSelectAdd = (target: any) => {
  if (!!target) {
    fetchPayOrderList(target)
    fetchOrderGroupList(target)
    fetchTypeList(target)
    fetchBuildingList(target)
    fetchContractList({
      project: target,
      ordering: 'contractor__name',
    })
    fetchSalePriceList({ project: target })
    fetchDownPayList({ project: target })
  } else {
    contractStore.orderGroupList = []
    contractStore.contractList = []
    contractStore.contractsCount = 0
    contractStore.salesPriceList = []
    contractStore.downPaymentList = []

    paymentStore.payOrderList = []
    projectDataStore.unitTypeList = []
    projectDataStore.buildingList = []
  }
}

const pageSelect = (page: number) => {
  ctor_ids.value = []
  listControl.value.listFiltering(page)
}

const listFiltering = (payload: any) => {
  ctor_ids.value = []
  fetchContractList({ ...{ project: project.value }, ...payload })
}

const onCtorChk = (payload: { chk: boolean; pk: number }) => {
  const contractors: number[] = ctor_ids.value
  if (payload.chk) {
    if (!contractors.includes(payload.pk)) contractors.push(payload.pk)
  } else {
    let i = contractors.indexOf(payload.pk)
    contractors.splice(i, 1)
  }
}

const allUnChecked = () => {
  ctor_ids.value = []
}

const getNowOrder = (orderPk: string) => {
  fetchPayOrder(orderPk)
}

const setPubDate = (payload: any) => {
  print_data.pub_date = payload
}

const onSubmit = (payload: any) => {
  const { pk, now_payment_order } = payload
  const { now_due_date, ...bill_data } = payload
  if (pk) {
    patchPayOrder({
      pk: now_payment_order,
      pay_due_date: now_due_date,
    })
    patchSalesBillIssue(bill_data)
  } else {
    patchPayOrder({
      pk: now_payment_order,
      pay_due_date: now_due_date,
    })
    createSalesBillIssue(bill_data)
  }
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <SalesBillIssueForm
        :bill-issue="billIssue"
        @get-now-order="getNowOrder"
        @set-pub-date="setPubDate"
        @on-submit="onSubmit"
      />
      <ListController
        ref="listControl"
        :now-order-name="payOrderName"
        @list-filtering="listFiltering"
      />
      <DownloadButton :print-data="print_data" :contractors="ctor_ids" />
      <ContractList
        ref="contractList"
        :now-order="payOrderTime"
        @on-ctor-chk="onCtorChk"
        @page-select="pageSelect"
        @all-un-checked="allUnChecked"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
