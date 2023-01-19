<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/proCash/_menu/headermixin'
import { useProject } from '@/store/pinia/project'
import { CashBookFilter, useProCash } from '@/store/pinia/proCash'
import { ProjectCashBook as PrCashBook } from '@/store/types/proCash'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/proCash/Imprest/components/ListController.vue'
import AddProImprest from '@/views/proCash/Imprest/components/AddProImprest.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ProImprestList from '@/views/proCash/Imprest/components/ProImprestList.vue'

const listControl = ref()

const dataFilter = ref<CashBookFilter>({
  page: 1,
  from_date: '',
  to_date: '',
  sort: null,
  pro_acc_d1: null,
  pro_acc_d2: null,
  bank_account: null,
  search: '',
})

const excelUrl = computed(() => {
  const pj = project.value
  const sd = dataFilter.value.from_date
  const ed = dataFilter.value.to_date
  const st = dataFilter.value.sort || ''
  const d1 = dataFilter.value.pro_acc_d1 || ''
  const d2 = dataFilter.value.pro_acc_d2 || ''
  const ba = dataFilter.value.bank_account || ''
  const q = dataFilter.value.search
  return `/excel/p-cashbook/?project=${pj}&imp=1&sdate=${sd}&edate=${ed}&sort=${st}&d1=${d1}&d2=${d2}&bank_acc=${ba}&q=${q}`
})

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const proCashStore = useProCash()
const fetchProAccSortList = () => proCashStore.fetchProAccSortList
const fetchProAllAccD1List = () => proCashStore.fetchProAllAccD1List
const fetchProAllAccD2List = () => proCashStore.fetchProAllAccD2List

const fetchProFormAccD1List = (sort?: number | null) =>
  proCashStore.fetchProFormAccD1List(sort)
const fetchProFormAccD2List = (d1?: number | null, sort?: number | null) =>
  proCashStore.fetchProFormAccD2List(d1, sort)

const fetchProBankAccList = (projId: number) =>
  proCashStore.fetchProBankAccList(projId)
const fetchProjectImprestList = (payload: { project: number }) =>
  proCashStore.fetchProjectImprestList(payload)

const createPrCashBook = (
  payload: PrCashBook & { sepData: PrCashBook | null } & {
    filters: CashBookFilter
  },
) => proCashStore.createPrCashBook(payload)

const updatePrImprestBook = (
  payload: PrCashBook & { sepData: PrCashBook | null } & {
    filters: CashBookFilter
  },
) => proCashStore.updatePrImprestBook(payload)

const deletePrImprestBook = (
  payload: { pk: number; project: number } & {
    filters?: CashBookFilter
  },
) => proCashStore.deletePrImprestBook(payload)

onBeforeMount(() => {
  fetchProAccSortList()
  fetchProAllAccD1List()
  fetchProAllAccD2List()
  fetchProFormAccD1List()
  fetchProFormAccD2List()
  fetchProBankAccList(initProjId.value)
  fetchProjectImprestList({ project: initProjId.value })
})

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchProBankAccList(target)
    fetchProjectImprestList({ project: target })
  } else {
    proCashStore.balanceByAccList = []
    proCashStore.proImprestList = []
    proCashStore.proImprestCount = 0
  }
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  listControl.value.listFiltering(page)
}

const listFiltering = (payload: CashBookFilter) => {
  dataFilter.value = payload
  const sort = payload.sort ? payload.sort : null
  const d1 = payload.pro_acc_d1 ? payload.pro_acc_d1 : null
  fetchProFormAccD1List(sort)
  fetchProFormAccD2List(d1, sort)
  fetchProjectImprestList({ ...{ project: project.value }, ...payload })
}

const onCreate = (
  payload: PrCashBook & { sepData: PrCashBook | null } & {
    filters: CashBookFilter
  } & { bank_account_to: null | number; ba_is_imprest: boolean },
) => {
  payload.project = project.value
  if (payload.sort === 3 && payload.bank_account_to) {
    const { bank_account_to, ba_is_imprest, income, ...inputData } = payload

    createPrCashBook(inputData)

    delete inputData.outlay
    if (!ba_is_imprest) inputData.is_imprest = ba_is_imprest
    inputData.bank_account = bank_account_to

    createPrCashBook({ ...{ income }, ...inputData })
  } else createPrCashBook(payload)
}

const onUpdate = (
  payload: PrCashBook & { sepData: PrCashBook | null } & {
    filters: CashBookFilter
  },
) => updatePrImprestBook(payload)

const multiSubmit = (payload: {
  formData: PrCashBook & {
    bank_account_to: null | number
    ba_is_imprest: boolean
  }
  sepData: PrCashBook | null
}) => {
  const { formData, ...sepData } = payload
  const submitData = {
    ...formData,
    ...sepData,
    ...{ filters: dataFilter.value },
  }

  if (formData.pk) onUpdate(submitData)
  else onCreate(submitData)
}

const onDelete = (payload: { pk: number; project: number }) =>
  deletePrImprestBook({ ...{ filters: dataFilter.value }, ...payload })
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddProImprest @multi-submit="multiSubmit" />
      <TableTitleRow
        title="프로젝트 전도금 내역"
        color="success"
        excel
        :url="excelUrl"
      />
      <ProImprestList
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
