<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
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

watch(project, val => {
  if (!!val) dataSet(val)
  else dataReset()
})

const fetchIncBudgetList = (proj: number) => projStore.fetchIncBudgetList(proj)

const prDataStore = useProjectData()
const fetchTypeList = (proj: number) => prDataStore.fetchTypeList(proj)

const contStore = useContract()
const fetchOrderGroupList = (proj: number) =>
  contStore.fetchOrderGroupList(proj)
const fetchContSummaryList = (proj: number, date?: string) =>
  contStore.fetchContSummaryList(proj, date)

const payStore = usePayment()
const fetchPaySumList = (proj: number, date?: string) =>
  payStore.fetchPaySumList(proj, date)

const dataSet = (pk: number) => {
  fetchTypeList(pk)
  fetchOrderGroupList(pk)
  fetchContSummaryList(pk)
  fetchIncBudgetList(pk)
  fetchPaySumList(pk)
}

const dataReset = () => {
  prDataStore.unitTypeList = []
  contStore.orderGroupList = []
  contStore.contSummaryList = []
  projStore.proIncBudgetList = []
  payStore.paySumList = []
}

const setDate = (d: Date) => {
  date.value = new Date(d)
  if (project.value) {
    fetchPaySumList(project.value, dateFormat(date.value))
    fetchContSummaryList(project.value, dateFormat(date.value))
  }
}

onBeforeMount(() => {
  const projectPk = project.value || projStore.initProjId
  fetchTypeList(projectPk)
  fetchOrderGroupList(projectPk)
  fetchContSummaryList(projectPk)
  fetchIncBudgetList(projectPk)
  fetchPaySumList(projectPk)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <DateChoicer @set-date="setDate" />

      <TableTitleRow excel :url="excelUrl" :disabled="!project" />
      <PaymentStatus :date="dateFormat(date)" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
