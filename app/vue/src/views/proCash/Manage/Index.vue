<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { useProCash } from '@/store/pinia/proCash'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/proCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/proCash/Manage/components/ListController.vue'
import AddProCash from '@/views/proCash/Manage/components/AddProCash.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ProCashList from '@/views/proCash/Manage/components/ProCashList.vue'

const dataFilter = ref({
  page: 1,
  from_date: '',
  to_date: '',
  sort: '',
  pro_acc_d1: '',
  pro_acc_d2: '',
  bank_account: '',
  search: '',
})

const projectStore = useProject()

const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const proCashStore = useProCash()
const fetchProAccSortList = () => proCashStore.fetchProAccSortList
const fetchProAllAccD1List = () => proCashStore.fetchProAllAccD1List
const fetchProAllAccD2List = () => proCashStore.fetchProAllAccD2List
const fetchProFormAccD1List = (sort?: string) =>
  proCashStore.fetchProFormAccD1List(sort)
const fetchProFormAccD2List = (d1?: string, sort?: string) =>
  proCashStore.fetchProFormAccD2List(d1, sort)
const fetchProBankAccList = (projId: number) =>
  proCashStore.fetchProBankAccList(projId)
const fetchProjectCashList = (payload: { project: number }) =>
  proCashStore.fetchProjectCashList(payload)

const createPrCashBook = (payload: any) =>
  proCashStore.createPrCashBook(payload)
const updatePrCashBook = (payload: any) =>
  proCashStore.updatePrCashBook(payload)
const deletePrCashBook = (payload: any) =>
  proCashStore.deletePrCashBook(payload)

onBeforeMount(() => {
  fetchProAccSortList()
  fetchProAllAccD1List()
  fetchProAllAccD2List()
  fetchProFormAccD1List()
  fetchProFormAccD2List()
  fetchProBankAccList(initProjId.value)
  fetchProjectCashList({ project: initProjId.value })
})

const onSelectAdd = (target: any) => {
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

const listFiltering = (payload: any) => {
  dataFilter.value = payload
  const sort = payload.sort ? payload.sort : ''
  const d1 = payload.pro_acc_d1 ? payload.pro_acc_d1 : ''
  fetchProFormAccD1List(sort)
  fetchProFormAccD2List(d1, sort)
  fetchProjectCashList({ ...{ project: project.value }, ...payload })
}
const onCreate = (payload: any) => {
  payload.project = project.value
  if (payload.sort === '3' && payload.bank_account_to) {
    const { bank_account_to, income, ...inputData } = payload
    createPrCashBook(inputData)

    delete inputData.bank_account
    delete inputData.outlay

    createPrCashBook({
      ...{ bank_account: bank_account_to, income },
      ...inputData,
    })
  } else createPrCashBook(payload)
}

const onUpdate = (payload: any) =>
  updatePrCashBook({ ...{ filters: dataFilter.value }, ...payload })

const multiSubmit = (payload: any) => {
  const { formData, sepData } = payload
  console.log(formData, sepData)
  if (formData.sort) {
    if (formData.pk) onUpdate(formData)
    else onCreate(formData)
  }
  if (sepData.sort) {
    if (sepData.pk) onUpdate(sepData)
    else onCreate({ ...{ filters: dataFilter.value }, ...sepData })
  }
}

const onDelete = (payload: any) =>
  deletePrCashBook({ ...{ filters: dataFilter.value }, ...payload })
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
