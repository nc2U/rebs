<script lang="ts" setup>
import Cookies from 'js-cookie'
import { ref, computed, onBeforeMount, onMounted, onUpdated, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/payments/_menu/headermixin'
import { dateFormat } from '@/utils/baseMixins'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { type Contract } from '@/store/types/contract'
import { type ContFilter, useContract } from '@/store/pinia/contract'
import { useProCash } from '@/store/pinia/proCash'
import { type ProjectCashBook, type CashBookFilter } from '@/store/types/proCash'
import { type DownPayFilter, type PriceFilter, usePayment } from '@/store/pinia/payment'
import { useRouter, useRoute, onBeforeRouteLeave } from 'vue-router'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContChoicer from '@/views/payments/Register/components/ContChoicer.vue'
import PaymentListAll from '@/views/payments/Register/components/PaymentListAll.vue'
import OrdersBoard from '@/views/payments/Register/components/OrdersBoard.vue'
import CreateButton from '@/views/payments/Register/components/CreateButton.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import DatePicker from '@/components/DatePicker/index.vue'

const paymentId = ref<string>('')
const date = ref(dateFormat(new Date()))

const pdfPayConf = ref(Cookies.get('pdfPayConf') ?? '1')

watch(pdfPayConf, newVal => Cookies.set('pdfPayConf', newVal))

const paymentUrl = computed(() => {
  const url = '/pdf/payments/'
  const proj = project.value ?? ''
  const cont = contract.value?.pk ?? ''
  return `${url}?project=${proj}&contract=${cont}&sel=${pdfPayConf.value}&pub_date=${date.value ?? ''}`
})

const calcUrl = computed(() => {
  const url = '/pdf/calculation/'
  const proj = project.value ?? ''
  const cont = contract.value?.pk ?? ''
  return `${url}?project=${proj}&contract=${cont}&pub_date=${date.value ?? ''}`
})

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const contractStore = useContract()
const contract = computed(() => contractStore.contract)

const paymentStore = usePayment()
const AllPaymentList = computed(() => paymentStore.AllPaymentList)

const projectDataStore = useProjectData()
const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)

const fetchAllPaymentList = (payload: CashBookFilter) => paymentStore.fetchAllPaymentList(payload)
const fetchPayOrderList = (projId: number) => paymentStore.fetchPayOrderList(projId)
const fetchDownPayList = (payload: DownPayFilter) => paymentStore.fetchDownPayList(payload)
const fetchPriceList = (payload: PriceFilter) => paymentStore.fetchPriceList(payload)

const proCashStore = useProCash()
const fetchAllProBankAccList = (projId: number) => proCashStore.fetchAllProBankAccList(projId)
const createPrCashBook = (
  payload: ProjectCashBook & { sepData: ProjectCashBook | null } & {
    filters: CashBookFilter
  },
) => proCashStore.createPrCashBook(payload)
const updatePrCashBook = (
  payload: ProjectCashBook & {
    sepData: ProjectCashBook | null
  } & { isPayment?: boolean } & {
    filters: CashBookFilter
  },
) => proCashStore.updatePrCashBook(payload)
const deletePrCashBook = (
  payload: { pk: number; project: number; contract: number } & {
    filters: CashBookFilter
  },
) => proCashStore.deletePrCashBook(payload)

const fetchContractList = (payload: ContFilter) => contractStore.fetchContractList(payload)
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

const onContFiltering = (payload: ContFilter) => {
  payload.project = project.value
  if (payload.project) fetchContractList({ ...payload })
}

const getContract = (cont: number) => {
  router.replace({
    name: '건별 수납 관리',
    query: { contract: cont },
  })
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
  updatePrCashBook({ ...payload, isPayment: true })
}

const onDelete = (pk: number) => {
  const delFilter = {
    pk,
    project: project.value || 1,
    contract: contract.value?.pk || 1,
  }
  deletePrCashBook({ ...delFilter, ...{ filters: {} } })
}

const dataSetup = (pk: number) => {
  fetchTypeList(pk)
  fetchPayOrderList(pk)
  fetchAllProBankAccList(pk)
}

const dataReset = () => {
  contractStore.contract = null
  contractStore.contractList = []
  projectDataStore.unitTypeList = []
  paymentStore.AllPaymentList = []
  paymentStore.payOrderList = []
  proCashStore.proBankAccountList = []
}

const projSelect = (target: number | null) => {
  router.replace({ name: '건별 수납 관리' })
  dataReset()
  if (!!target) dataSetup(target)
}

onBeforeMount(() => {
  dataSetup(project.value || projStore.initProjId)
  if (route.query.payment) paymentId.value = route.query.payment as string
})

onMounted(() => {
  if (route.query.contract) {
    router.replace({
      name: '건별 수납 관리',
      query: { contract: route.query.contract },
    })
    const cont = Number(route.query.contract)
    fetchContract(cont)
  } else {
    contractStore.contract = null
    paymentStore.AllPaymentList = []
  }
})

onUpdated(() => {
  if (route.query.contract) {
    router.replace({
      name: '건별 수납 관리',
      query: { contract: route.query.contract },
    })
    const cont = Number(route.query.contract)
    fetchContract(cont)
  }
})

onBeforeRouteLeave(() => {
  contractStore.contract = null
  paymentStore.AllPaymentList = []
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="ProjectSelect"
    @proj-select="projSelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContChoicer
        ref="listControl"
        :project="project || undefined"
        :contract="contract as Contract"
        :payment-url="paymentUrl"
        @list-filtering="onContFiltering"
        @get-contract="getContract"
      />
      <TableTitleRow :disabled="!project || !contract" pdf :url="paymentUrl">
        <v-radio-group
          v-model="pdfPayConf"
          inline
          size="sm"
          density="compact"
          color="success"
          class="d-flex flex-row-reverse"
          style="font-size: 0.8em"
          :disabled="!project"
        >
          <span v-show="project && contract" class="mr-3">
            <DatePicker v-model="date" placeholder="발행일자" />
            <v-tooltip activator="parent" location="right">발행일자</v-tooltip>
          </span>

          <v-btn
            v-if="project === 1"
            :href="calcUrl"
            flat
            :disabled="!project || !contract"
            color="light"
            size="small"
            class="mt-1 mr-2"
            style="text-decoration: none"
          >
            가산(할인) 내역
          </v-btn>

          <v-radio label="일반내역" value="1" class="mt-1" />
          <v-radio label="담당확인" value="2" class="mt-1" />
        </v-radio-group>
      </TableTitleRow>
      <CRow>
        <CCol lg="7">
          <PaymentListAll
            :contract="contract as Contract"
            :payment-id="paymentId"
            :payment-list="AllPaymentList"
            @on-update="onUpdate"
            @on-delete="onDelete"
          />

          <CreateButton :contract="contract as Contract" @on-create="onCreate" />
        </CCol>
        <CCol lg="5">
          <OrdersBoard :contract="contract as Contract" :payment-list="AllPaymentList" />
        </CCol>
      </CRow>
    </CCardBody>
  </ContentBody>
</template>
