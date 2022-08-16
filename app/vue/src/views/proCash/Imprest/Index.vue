<script lang="ts" setup>
import { computed, ref, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/proCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/proCash/Imprest/components/ListController.vue'
import AddProImprest from '@/views/proCash/Imprest/components/AddProImprest.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ProImprestList from '@/views/proCash/Imprest/components/ProImprestList.vue'

const listControl = ref()

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

const store = useStore()
const projectStore = useProject()

const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const fetchProAccSortList = () => store.dispatch('proCash/fetchProAccSortList')

const fetchProAllAccD1List = () =>
  store.dispatch('proCash/fetchProAllAccD1List')
const fetchProAllAccD2List = () =>
  store.dispatch('proCash/fetchProAllAccD2List')

const fetchProFormAccD1List = (sort?: string) =>
  store.dispatch('proCash/fetchProFormAccD1List', sort)
const fetchProFormAccD2List = (payload?: { d1: string; sort: string }) =>
  store.dispatch('proCash/fetchProFormAccD2List', payload)

const fetchProBankAccList = (projId: number) =>
  store.dispatch('proCash/fetchProBankAccList', projId)
const fetchProjectImprestList = (payload: { project: number } & any) =>
  store.dispatch('proCash/fetchProjectImprestList', payload)

const createPrCashBook = (payload: any) =>
  store.dispatch('proCash/createPrCashBook', payload)
const updatePrCashBook = (payload: any) =>
  store.dispatch('proCash/updatePrCashBook', payload)
const deletePrCashBook = (payload: any) =>
  store.dispatch('proCash/deletePrCashBook', payload)

onBeforeMount(() => {
  fetchProAccSortList()
  fetchProAllAccD1List()
  fetchProAllAccD2List()
  fetchProFormAccD1List()
  fetchProFormAccD2List()
  fetchProBankAccList(initProjId.value)
  fetchProjectImprestList({ project: initProjId.value })
})

const onSelectAdd = (target: any) => {
  if (!!target) {
    fetchProBankAccList(target)
    fetchProjectImprestList({ project: target })
  } else {
    store.commit('proCash/updateState', {
      balanceByAccList: [],
      proImprestList: [],
      proImprestCount: 0,
    })
  }
}
const pageSelect = (page: number) => {
  dataFilter.value.page = page
  listControl.value.listFiltering(page)
}
const listFiltering = (payload: any) => {
  dataFilter.value = payload
  const sort = payload.sort ? payload.sort : ''
  const d1 = payload.pro_acc_d1 ? payload.pro_acc_d1 : ''
  fetchProFormAccD1List(sort)
  fetchProFormAccD2List({ d1, sort })
  fetchProjectImprestList({ ...{ project: project.value }, ...payload })
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
      <AddProImprest @multi-submit="multiSubmit" />
      <TableTitleRow
        title="프로젝트 전도금 내역"
        color="success"
        excel
        disabled
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
