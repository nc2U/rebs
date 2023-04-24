<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/payments/_menu/headermixin'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { ContFilter, useContract } from '@/store/pinia/contract'
import { useProCash } from '@/store/pinia/proCash'
import { ProjectCashBook, CashBookFilter } from '@/store/types/proCash'
import { DownPayFilter, PriceFilter, usePayment } from '@/store/pinia/payment'
import { useRouter, useRoute, onBeforeRouteLeave } from 'vue-router'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContChoicer from '@/views/payments/Register/components/ContChoicer.vue'
import PaymentListAll from '@/views/payments/Register/components/PaymentListAll.vue'
import OrdersBoard from '@/views/payments/Register/components/OrdersBoard.vue'
import CreateButton from '@/views/payments/Register/components/CreateButton.vue'

const paymentId = ref<string>('')

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const contractStore = useContract()
const contract = computed(() => contractStore.contract)

const paymentStore = usePayment()
const AllPaymentList = computed(() => paymentStore.AllPaymentList)

const projectDataStore = useProjectData()
const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)

const fetchAllPaymentList = (payload: CashBookFilter) =>
  paymentStore.fetchAllPaymentList(payload)
const fetchPayOrderList = (projId: number) =>
  paymentStore.fetchPayOrderList(projId)
const fetchDownPayList = (payload: DownPayFilter) =>
  paymentStore.fetchDownPayList(payload)
const fetchPriceList = (payload: PriceFilter) =>
  paymentStore.fetchPriceList(payload)

const proCashStore = useProCash()
const fetchAllProBankAccList = (projId: number) =>
  proCashStore.fetchAllProBankAccList(projId)
const createPrCashBook = (
  payload: ProjectCashBook & { sepData: ProjectCashBook | null } & {
    filters: CashBookFilter
  },
) => proCashStore.createPrCashBook(payload)
const updatePrCashBook = (
  payload: ProjectCashBook & { sepData: ProjectCashBook | null } & {
    filters: CashBookFilter
  },
) => proCashStore.updatePrCashBook(payload)
const deletePrCashBook = (
  payload: { pk: number; project: number; contract: number } & {
    filters: CashBookFilter
  },
) => proCashStore.deletePrCashBook(payload)

const fetchContractList = (payload: ContFilter) =>
  contractStore.fetchContractList(payload)
const fetchContract = (pk: number) => contractStore.fetchContract(pk)

const [route, router] = [useRoute(), useRouter()]

watch(contract, newVal => {
  if (newVal && project.value) {
    const order_group = newVal.order_group
    const unit_type = newVal.unit_type
    fetchPriceList({ project: project.value, order_group, unit_type })
    fetchDownPayList({ project: project.value, order_group, unit_type })
    fetchAllPaymentList({
      project: project.value,
      contract: newVal.pk,
      ordering: 'deal_date',
    })
  } else {
    paymentStore.priceList = []
    paymentStore.downPayList = []
    paymentStore.AllPaymentList = []
  }
})

const onSelectAdd = (target: number) => {
  router.push({ name: '건별 수납 관리' })
  contractStore.contract = null
  contractStore.contractList = []
  projectDataStore.unitTypeList = []
  paymentStore.AllPaymentList = []
  paymentStore.payOrderList = []
  proCashStore.proBankAccountList = []
  if (!!target) {
    fetchTypeList(target)
    fetchPayOrderList(target)
    fetchAllProBankAccList(target)
  }
}

const onContFiltering = (payload: ContFilter) => {
  payload.project = project.value
  if (payload.project) fetchContractList({ ...payload })
}

const getContract = (cont: number) => {
  router.replace({
    name: '건별 수납 관리',
    query: { contract: cont },
  })
  fetchContract(cont)
}

const onCreate = (
  payload: ProjectCashBook & { sepData: ProjectCashBook | null } & {
    filters: CashBookFilter
  },
) => {
  if (project.value) payload.project = project.value
  createPrCashBook(payload)
}

const onUpdate = (
  payload: ProjectCashBook & { sepData: ProjectCashBook | null } & {
    filters: CashBookFilter
  },
) => {
  if (project.value) payload.project = project.value
  updatePrCashBook(payload)
}

const onDelete = (pk: number) => {
  const delFilter = {
    pk,
    project: project.value || 1,
    contract: contract.value?.pk || 1,
  }
  deletePrCashBook({ ...delFilter, ...{ filters: {} } })
}

onBeforeMount(() => {
  if (route.query.contract) {
    router.replace({
      name: '건별 수납 관리',
      query: { contract: route.query.contract },
    })
    const cont = Number(route.query.contract)
    getContract(cont)
  }
  if (route.query.payment) paymentId.value = route.query.payment as string

  if (initProjId.value) {
    fetchTypeList(initProjId.value)
    fetchPayOrderList(initProjId.value)
    fetchAllProBankAccList(initProjId.value)
  }
})

onBeforeRouteLeave(() => {
  contractStore.contract = null
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
