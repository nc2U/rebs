<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { navMenu, pageTitle } from '@/views/payments/_menu/headermixin'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/payments/Status/components/DateChoicer.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import PaymentStatus from './components/PaymentStatus.vue'

const date = ref(new Date())
const sort = ref<null | '2' | '1' | '0'>('2')

const excelUrl = computed(() => '')

const projStore = useProject()
const initProjId = computed(() => projStore.initProjId)
const project = computed(() => projStore.project?.pk || initProjId.value)

const prDataStore = useProjectData()
const unitType = computed(() => prDataStore.unitTypeList)

const contStore = useContract()
const orderGroup = computed(() => contStore.orderGroupList)
const contSummaryList = computed(() => contStore.contSummaryList)

const fetchTypeList = (proj: number) => prDataStore.fetchTypeList(proj)

const fetchOrderGroupList = (proj: number) =>
  contStore.fetchOrderGroupList(proj)
const fetchContSummaryList = (proj: number) =>
  contStore.fetchContSummaryList(proj)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchTypeList(target)
    fetchOrderGroupList(target)
    fetchContSummaryList(target)
  } else {
    prDataStore.unitTypeList = []
    contStore.orderGroupList = []
    contStore.contSummaryList = []
  }
}

const setDate = (d: Date) => (date.value = new Date(d))
const setSort = (s: null | '2' | '1' | '0') => (sort.value = s)

onBeforeMount(() => {
  fetchTypeList(project.value)
  fetchOrderGroupList(project.value)
  fetchContSummaryList(project.value)
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
      <DateChoicer @set-date="setDate" @set-sort="setSort" />

      <TableTitleRow excel :url="excelUrl" :disabled="true" />
      <PaymentStatus
        :date="date"
        :sort="sort"
        :order-group="orderGroup"
        :unit-type="unitType"
        :cont-sum="contSummaryList"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
