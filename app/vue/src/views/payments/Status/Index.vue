<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { navMenu, pageTitle } from '@/views/payments/_menu/headermixin'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { usePayment } from '@/store/pinia/payment'
import { dateFormat } from '@/utils/baseMixins'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/payments/Status/components/DateChoicer.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import PaymentStatus from './components/PaymentStatus.vue'

const date = ref(new Date())

const excelUrl = computed(
  () =>
    `/excel/paid-status/?project=${project.value}&date=${dateFormat(
      date.value,
    )}`,
)

const projStore = useProject()
const project = computed(() => projStore.project?.pk)
const initProjId = computed(() => projStore.initProjId)

const fetchIncBudgetList = (proj: number) => projStore.fetchIncBudgetList(proj)

const prDataStore = useProjectData()
const fetchTypeList = (proj: number) => prDataStore.fetchTypeList(proj)

const contStore = useContract()
const fetchOrderGroupList = (proj: number) =>
  contStore.fetchOrderGroupList(proj)
const fetchContSummaryList = (proj: number, date?: string) =>
  contStore.fetchContSummaryList(proj, date)

const paymentStore = usePayment()
const fetchPaySumList = (proj: number, date?: string) =>
  paymentStore.fetchPaySumList(proj, date)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchTypeList(target)
    fetchOrderGroupList(target)
    fetchContSummaryList(target)
    fetchIncBudgetList(target)
    fetchPaySumList(target)
  } else {
    prDataStore.unitTypeList = []
    contStore.orderGroupList = []
    contStore.contSummaryList = []
    projStore.proIncBudgetList = []
    paymentStore.paySumList = []
  }
}

const setDate = (d: Date) => {
  date.value = new Date(d)
  if (project.value) {
    fetchPaySumList(project.value, dateFormat(date.value))
    fetchContSummaryList(project.value, dateFormat(date.value))
  }
}

onBeforeMount(() => {
  if (initProjId.value) {
    fetchTypeList(initProjId.value)
    fetchOrderGroupList(initProjId.value)
    fetchContSummaryList(initProjId.value)
    fetchIncBudgetList(initProjId.value)
    fetchPaySumList(initProjId.value)
  }
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
      <DateChoicer @set-date="setDate" />

      <TableTitleRow excel :url="excelUrl" :disabled="!project" />
      <PaymentStatus :date="dateFormat(date)" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
