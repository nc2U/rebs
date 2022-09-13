<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { navMenu, pageTitle } from '@/views/comCash/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { useComCash, DataFilter as Filter } from '@/store/pinia/comCash'
import { CashBook } from '@/store/types/comCash'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/comCash/Manage/components/ListController.vue'
import AddCash from '@/views/comCash/Manage/components/AddCash.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import CashesList from '@/views/comCash/Manage/components/CashesList.vue'
import { CashBookFilter } from '@/store/pinia/proCash'

const listControl = ref()

const dataFilter = ref<Filter>({
  page: 1,
  company: null,
  from_date: '',
  to_date: '',
  sort: '',
  account_d1: '',
  account_d2: '',
  account_d3: '',
  bank_account: '',
  search: '',
})

const companyStore = useCompany()
const initComId = computed(() => companyStore.initComId)
const company = computed(() => companyStore.company?.pk || initComId.value)

const comCashStore = useComCash()
const fetchCompany = (pk: number) => companyStore.fetchCompany(pk)
const fetchAccSortList = () => comCashStore.fetchAccSortList()
const fetchAllAccD1List = () => comCashStore.fetchAllAccD1List()
const fetchAllAccD2List = () => comCashStore.fetchAllAccD2List()
const fetchAllAccD3List = () => comCashStore.fetchAllAccD3List()
const fetchFormAccD1List = (sort: string) =>
  comCashStore.fetchFormAccD1List(sort)
const fetchFormAccD2List = (sort: string, d1: string) =>
  comCashStore.fetchFormAccD2List(sort, d1)
const fetchFormAccD3List = (sort: string, d1: string, d2: string) =>
  comCashStore.fetchFormAccD3List(sort, d1, d2)
const fetchComBankAccList = (pk: number) => comCashStore.fetchComBankAccList(pk)

const fetchCashBookList = (payload: Filter) =>
  comCashStore.fetchCashBookList(payload)
const createCashBook = (payload: CashBook) =>
  comCashStore.createCashBook(payload)
const updateCashBook = (payload: CashBook) =>
  comCashStore.updateCashBook(payload)
const deleteCashBook = (payload: CashBook & { filters: Filter }) =>
  comCashStore.deleteCashBook(payload)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchCompany(target)
    fetchComBankAccList(target)
    fetchCashBookList({ company: target })
  } else {
    companyStore.company = null
    comCashStore.comBankList = []
    comCashStore.cashBookList = []
    comCashStore.cashBookCount = 0
  }
}

const pageSelect = (page: number) => listControl.value.listFiltering(page)

const listFiltering = (payload: Filter) => {
  if (company.value) payload.company = company.value
  dataFilter.value = payload
  const sort = payload.sort ? payload.sort : ''
  const d1 = payload.account_d1 ? payload.account_d1 : ''
  const d2 = payload.account_d2 ? payload.account_d2 : ''
  fetchFormAccD1List(sort)
  fetchFormAccD2List(sort, d1)
  fetchFormAccD3List(sort, d1, d2)

  fetchCashBookList(payload)
}

const onCreate = (
  payload: CashBook & { filters: Filter } & { bank_account_to?: number },
) => {
  payload.company = company.value
  if (payload.sort === 3 && payload.bank_account_to) {
    const { bank_account_to, income, ...inputData } = payload

    createCashBook(inputData)

    delete inputData.outlay
    inputData.bank_account = bank_account_to

    createCashBook({ ...{ income }, ...inputData })
  } else createCashBook(payload)
}

const onUpdate = (payload: CashBook & { filters: Filter }) =>
  updateCashBook(payload)

const multiSubmit = (payload: {
  formData: CashBook
  sepData: CashBook | null
}) => {
  const { formData, sepData } = payload

  const mainFormData = { ...{ filters: dataFilter.value }, ...formData }

  if (formData.pk) onUpdate(mainFormData)
  else onCreate(mainFormData)

  if (sepData) {
    const separatedData = { ...{ filters: dataFilter.value }, ...sepData }
    if (sepData.pk) onUpdate(separatedData)
    else onCreate(separatedData)
  }
}

const onDelete = (payload: CashBook) =>
  deleteCashBook({ ...{ filters: dataFilter.value }, ...payload })

onBeforeMount(() => {
  fetchCompany(initComId.value)
  fetchAccSortList()
  fetchAllAccD1List()
  fetchAllAccD2List()
  fetchAllAccD3List()
  fetchFormAccD1List('')
  fetchFormAccD2List('', '')
  fetchFormAccD3List('', '', '')
  fetchComBankAccList(initComId.value)
  fetchCashBookList({ company: initComId.value })
  dataFilter.value.company = initComId.value
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
      <AddCash @multi-submit="multiSubmit" />
      <TableTitleRow title="본사 입출금 관리" color="indigo" excel disabled />
      <CashesList
        :company="company"
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
