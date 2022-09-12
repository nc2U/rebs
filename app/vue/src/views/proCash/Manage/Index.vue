<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/proCash/_menu/headermixin'
import { CashBookFilter, useProCash } from '@/store/pinia/proCash'
import { useProject } from '@/store/pinia/project'
import { ProjectCashBook } from '@/store/types/proCash'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/proCash/Manage/components/ListController.vue'
import AddProCash from '@/views/proCash/Manage/components/AddProCash.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ProCashList from '@/views/proCash/Manage/components/ProCashList.vue'

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
const fetchProjectCashList = (payload: { project: number }) =>
  proCashStore.fetchProjectCashList(payload)

const createPrCashBook = (
  payload: ProjectCashBook & { filters: CashBookFilter },
) => proCashStore.createPrCashBook(payload)
const updatePrCashBook = (
  payload: ProjectCashBook & { filters: CashBookFilter },
) => proCashStore.updatePrCashBook(payload)
const deletePrCashBook = (
  payload: { pk: number; project: number; contract: number } & {
    filters?: CashBookFilter
  },
) => proCashStore.deletePrCashBook(payload)

onBeforeMount(() => {
  fetchProAccSortList()
  fetchProAllAccD1List()
  fetchProAllAccD2List()
  fetchProFormAccD1List()
  fetchProFormAccD2List()
  fetchProBankAccList(initProjId.value)
  fetchProjectCashList({ project: initProjId.value })
})

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchProBankAccList(target)
    fetchProjectCashList({ project: target })
  } else {
    proCashStore.proBankAccountList = []
    proCashStore.proCashBookList = []
    proCashStore.proCashesCount = 0
  }
}

const listControl = ref()

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
  fetchProjectCashList({ ...{ project: project.value }, ...payload })
}
const onCreate = (
  payload: ProjectCashBook & { filters: CashBookFilter } & {
    bank_account_to: number
  },
) => {
  payload.project = project.value
  if (payload.sort === 3 && payload.bank_account_to) {
    const { bank_account_to, income, ...inputData } = payload

    createPrCashBook(inputData)

    delete inputData.outlay
    inputData.bank_account = bank_account_to

    createPrCashBook({ ...{ income }, ...inputData })
  } else createPrCashBook(payload)
}

const onUpdate = (payload: ProjectCashBook & { filters: CashBookFilter }) =>
  updatePrCashBook({ ...{ filters: dataFilter.value }, ...payload })

const multiSubmit = (payload: any) => {
  const { formData, sepData } = payload
  if (formData.sort) {
    if (formData.pk) onUpdate(formData)
    else onCreate(formData)
  }
  if (sepData.sort) {
    if (sepData.pk) onUpdate(sepData)
    else onCreate({ ...{ filters: dataFilter.value }, ...sepData })
  }
}

const onDelete = (
  payload: { pk: number; project: number; contract: number } & {
    filters?: CashBookFilter
  },
) => deletePrCashBook({ ...{ filters: dataFilter.value }, ...payload })
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
      <AddProCash @multi-submit="multiSubmit" />
      <TableTitleRow
        title="프로젝트 입출금 내역"
        color="indigo"
        excel
        disabled
      />
      <ProCashList
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
