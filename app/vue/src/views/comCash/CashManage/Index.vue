<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { navMenu, pageTitle } from '@/views/comCash/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import {
  useComCash,
  DataFilter as Filter,
  DataFilter,
} from '@/store/pinia/comCash'
import { CashBook, SepItems } from '@/store/types/comCash'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/comCash/CashManage/components/ListController.vue'
import AddCash from '@/views/comCash/CashManage/components/AddCash.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import CashesList from '@/views/comCash/CashManage/components/CashesList.vue'

const listControl = ref()

const dataFilter = ref<Filter>({
  page: 1,
  company: null,
  from_date: '',
  to_date: '',
  sort: null,
  account_d1: null,
  account_d2: null,
  account_d3: null,
  bank_account: null,
  search: '',
})

const excelUrl = computed(() => {
  const sd = dataFilter.value.from_date
  const ed = dataFilter.value.to_date
  const st = dataFilter.value.sort || ''
  const d1 = dataFilter.value.account_d1 || ''
  const d2 = dataFilter.value.account_d2 || ''
  const d3 = dataFilter.value.account_d3 || ''
  const ba = dataFilter.value.bank_account || ''
  const q = dataFilter.value.search
  return `/excel/cashbook/?s_date=${sd}&e_date=${ed}&sort=${st}&account_d1=${d1}&account_d2=${d2}&account_d3=${d3}&bank_account=${ba}&search_word=${q}`
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
const fetchFormAccD1List = (sort: number | null) =>
  comCashStore.fetchFormAccD1List(sort)
const fetchFormAccD2List = (sort: number | null, d1: number | null) =>
  comCashStore.fetchFormAccD2List(sort, d1)
const fetchFormAccD3List = (
  sort: number | null,
  d1: number | null,
  d2: number | null,
) => comCashStore.fetchFormAccD3List(sort, d1, d2)
const fetchComBankAccList = (pk: number) => comCashStore.fetchComBankAccList(pk)

const fetchCashBookList = (payload: Filter) =>
  comCashStore.fetchCashBookList(payload)
const createCashBook = (payload: CashBook & { sepData: SepItems | null }) =>
  comCashStore.createCashBook(payload)
const updateCashBook = (
  payload: CashBook & { sepData: SepItems | null } & { filters: DataFilter },
) => comCashStore.updateCashBook(payload)
const deleteCashBook = (payload: CashBook & { filters: Filter }) =>
  comCashStore.deleteCashBook(payload)
const patchAccD3 = (payload: { pk: number; is_hide: boolean }) =>
  comCashStore.patchAccD3(payload)

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
  const sort = payload.sort || null
  const d1 = payload.account_d1 || null
  const d2 = payload.account_d2 || null
  fetchFormAccD1List(sort)
  fetchFormAccD2List(sort, d1)
  fetchFormAccD3List(sort, d1, d2)

  fetchCashBookList(payload)
}

const onCreate = (
  payload: CashBook & { sepData: SepItems | null } & {
    bank_account_to?: number
  },
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

const onUpdate = (
  payload: CashBook & { sepData: SepItems | null } & { filters: Filter },
) => updateCashBook(payload)

const multiSubmit = (payload: {
  formData: CashBook
  sepData: SepItems | null
}) => {
  const { formData, ...sepData } = payload
  const createData = { ...formData, ...sepData }
  const updateData = { ...{ filters: dataFilter.value }, ...createData }

  if (formData.pk) onUpdate(updateData)
  else onCreate(createData)
}

const onDelete = (payload: CashBook) =>
  deleteCashBook({ ...{ filters: dataFilter.value }, ...payload })

const patchD3Hide = (payload: { pk: number; is_hide: boolean }) =>
  patchAccD3(payload)

onBeforeMount(() => {
  fetchCompany(initComId.value)
  fetchAccSortList()
  fetchAllAccD1List()
  fetchAllAccD2List()
  fetchAllAccD3List()
  fetchFormAccD1List(null)
  fetchFormAccD2List(null, null)
  fetchFormAccD3List(null, null, null)
  fetchComBankAccList(company.value)
  fetchCashBookList({ company: company.value })
  dataFilter.value.company = company.value
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
      <TableTitleRow
        title="본사 입출금 관리"
        color="indigo"
        excel
        :url="excelUrl"
      />
      <CashesList
        :company="company"
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @patchD3Hide="patchD3Hide"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
