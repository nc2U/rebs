<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useStore } from 'vuex'
import { useCompany } from '@/store/pinia/company'
import { navMenu, pageTitle } from '@/views/comCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/comCash/Manage/components/ListController.vue'
import AddCash from '@/views/comCash/Manage/components/AddCash.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import CashesList from '@/views/comCash/Manage/components/CashesList.vue'

const listControl = ref()
const dataFilter = ref({
  page: 1,
  from_date: '',
  to_date: '',
  sort: '',
  account_d1: '',
  account_d2: '',
  account_d3: '',
  bank_account: '',
  search: '',
})

const store = useStore()
const companyStore = useCompany()

const initComId = computed(() => companyStore.initComId.toString())
const company = computed(() => companyStore.company)

const fetchCompany = (pk: string) => companyStore.fetchCompany(pk)
const fetchAccSortList = () => store.dispatch('comCash/fetchAccSortList')
const fetchAllAccD1List = () => store.dispatch('comCash/fetchAllAccD1List')
const fetchAllAccD2List = () => store.dispatch('comCash/fetchAllAccD2List')
const fetchAllAccD3List = () => store.dispatch('comCash/fetchAllAccD3List')
const fetchFormAccD1List = (payload: { sort: string }) =>
  store.dispatch('comCash/fetchFormAccD1List', payload)
const fetchFormAccD2List = (payload: { sort: string; d1: string }) =>
  store.dispatch('comCash/fetchFormAccD2List', payload)
const fetchFormAccD3List = (payload: {
  sort: string
  d1: string
  d2: string
}) => store.dispatch('comCash/fetchFormAccD3List', payload)
const fetchComBankAccList = (pk: string) =>
  store.dispatch('comCash/fetchComBankAccList', pk)
const fetchCashBookList = (payload: any) =>
  store.dispatch('comCash/fetchCashBookList', payload)
const createCashBook = (payload: any) =>
  store.dispatch('comCash/createCashBook', payload)
const updateCashBook = (payload: any) =>
  store.dispatch('comCash/updateCashBook', payload)
const deleteCashBook = (payload: any) =>
  store.dispatch('comCash/deleteCashBook', payload)

const onSelectAdd = (target: any) => {
  if (!!target) {
    fetchCompany(target)
    fetchComBankAccList(target)
    fetchCashBookList({ company: target })
  } else {
    store.state.settings.company = null
    store.state.comCash.comBankList = []
    store.state.comCash.cashBookList = []
    store.state.comCash.cashBookCount = 0
  }
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  listControl.value.listFiltering(page)
}

const listFiltering = (payload: any) => {
  dataFilter.value = payload
  const pk = company.value?.pk.toString()
  const sort = payload.sort ? payload.sort : ''
  const d1 = payload.account_d1 ? payload.account_d1 : ''
  const d2 = payload.account_d2 ? payload.account_d2 : ''
  fetchFormAccD1List({ sort })
  fetchFormAccD2List({ sort, d1 })
  fetchFormAccD3List({ sort, d1, d2 })
  fetchCashBookList({ ...{ company: pk }, ...payload })
}

const onCreate = (payload: any) => {
  payload.company = company.value?.pk
  if (payload.sort === '3' && payload.bank_account_to) {
    const { bank_account_to, income, ...inputData } = payload

    createCashBook(inputData)

    delete inputData.bank_account
    delete inputData.outlay

    createCashBook({
      ...{ bank_account: bank_account_to, income },
      ...inputData,
    })
  } else createCashBook(payload)
}

const onUpdate = (payload: any) => {
  updateCashBook({ ...{ filters: dataFilter.value }, ...payload })
}

const onDelete = (payload: any) => {
  deleteCashBook({ ...{ filters: dataFilter.value }, ...payload })
}

onBeforeMount(() => {
  fetchAccSortList()
  fetchAllAccD1List()
  fetchAllAccD2List()
  fetchAllAccD3List()
  fetchFormAccD1List({ sort: '' })
  fetchFormAccD2List({ sort: '', d1: '' })
  fetchFormAccD3List({ sort: '', d1: '', d2: '' })
  fetchComBankAccList(initComId.value)
  fetchCashBookList({ company: initComId.value })
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="onSelectAdd"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddCash @on-create="onCreate" />
      <TableTitleRow title="본사 입출금 관리" color="indigo" excel disabled />
      <CashesList
        :company="company"
        @page-select="pageSelect"
        @on-update="onUpdate"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
