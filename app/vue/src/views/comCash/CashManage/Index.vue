<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { navMenu, pageTitle } from '@/views/comCash/_menu/headermixin'
import { cutString } from '@/utils/baseMixins'
import { useCompany } from '@/store/pinia/company'
import {
  useComCash,
  DataFilter as Filter,
  DataFilter,
} from '@/store/pinia/comCash'
import { CashBook, CompanyBank, SepItems } from '@/store/types/comCash'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/comCash/CashManage/components/ListController.vue'
import AddCash from '@/views/comCash/CashManage/components/AddCash.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import CashList from '@/views/comCash/CashManage/components/CashList.vue'

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

const comStore = useCompany()
const company = computed(() => comStore.company?.pk)
watch(company, val => (!!val ? dataSet(val) : dataReset()))

const fetchCompany = (pk: number) => comStore.fetchCompany(pk)
const fetchAllDepartList = (com: number) => comStore.fetchAllDepartList(com)

const cashStore = useComCash()
const fetchBankCodeList = () => cashStore.fetchBankCodeList()
const fetchAccSortList = () => cashStore.fetchAccSortList()
const fetchAllAccD1List = () => cashStore.fetchAllAccD1List()
const fetchAllAccD2List = () => cashStore.fetchAllAccD2List()
const fetchAllAccD3List = () => cashStore.fetchAllAccD3List()
const fetchFormAccD1List = (sort: number | null) =>
  cashStore.fetchFormAccD1List(sort)
const fetchFormAccD2List = (sort: number | null, d1: number | null) =>
  cashStore.fetchFormAccD2List(sort, d1)
const fetchFormAccD3List = (
  sort: number | null,
  d1: number | null,
  d2: number | null,
) => cashStore.fetchFormAccD3List(sort, d1, d2)
const fetchComBankAccList = (pk: number) => cashStore.fetchComBankAccList(pk)
const fetchAllComBankAccList = (pk: number) =>
  cashStore.fetchAllComBankAccList(pk)
const patchComBankAcc = (payload: CompanyBank) =>
  cashStore.patchComBankAcc(payload)

const fetchCashBookList = (payload: Filter) =>
  cashStore.fetchCashBookList(payload)
const createCashBook = (payload: CashBook & { sepData: SepItems | null }) =>
  cashStore.createCashBook(payload)
const updateCashBook = (
  payload: CashBook & { sepData: SepItems | null } & { filters: DataFilter },
) => cashStore.updateCashBook(payload)
const deleteCashBook = (payload: CashBook & { filters: Filter }) =>
  cashStore.deleteCashBook(payload)
const patchAccD3 = (payload: { pk: number; is_hide: boolean }) =>
  cashStore.patchAccD3(payload)

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
  if (company.value) fetchCashBookList(payload)
}

const chargeCreate = (
  payload: CashBook & { sepData: SepItems | null },
  charge: number,
) => {
  payload.sort = 2
  payload.account_d1 = 5
  payload.account_d2 = 17
  payload.account_d3 = 118
  payload.content = cutString(payload.content, 8) + ' - 이체수수료'
  payload.trader = '지급수수료'
  payload.outlay = charge
  payload.income = null
  payload.evidence = '0'
  payload.note = ''

  createCashBook(payload)
}

const onCreate = (
  payload: CashBook & { sepData: SepItems | null } & {
    bank_account_to: null | number
    charge: null | number
  },
) => {
  payload.company = company.value || null
  if (payload.sort === 3 && payload.bank_account_to) {
    // 대체 거래일 때
    const { bank_account_to, charge, ...inputData } = payload

    inputData.sort = 2
    inputData.trader = '내부대체'
    inputData.account_d3 = 131
    createCashBook(inputData)

    inputData.sort = 1
    inputData.account_d3 = 132
    inputData.income = inputData.outlay
    inputData.outlay = null
    inputData.bank_account = bank_account_to

    setTimeout(() => createCashBook({ ...inputData }), 300)
    if (!!charge) {
      setTimeout(() => chargeCreate({ ...inputData }, charge), 600)
    }
  } else if (payload.sort === 4) {
    // 취소 거래일 때
    payload.sort = 2
    payload.account_d3 = 133
    payload.evidence = '0'
    createCashBook(payload)
    payload.sort = 1
    payload.account_d3 = 134
    payload.income = payload.outlay
    payload.outlay = null
    payload.evidence = ''
    setTimeout(() => createCashBook(payload), 300)
  } else {
    const { charge, ...inputData } = payload
    createCashBook(inputData)
    if (!!charge) chargeCreate(inputData, charge)
  }
}

const onUpdate = (
  payload: CashBook & { sepData: SepItems | null } & { filters: Filter },
) => updateCashBook(payload)

const multiSubmit = (payload: {
  formData: CashBook
  sepData: SepItems | null
  bank_account_to: null | number
  charge: null | number
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

const onBankUpdate = (payload: CompanyBank) => patchComBankAcc(payload)

const dataSet = (pk: number) => {
  fetchCompany(pk)
  fetchAllDepartList(pk)
  fetchComBankAccList(pk)
  fetchAllComBankAccList(pk)
  fetchCashBookList({ company: pk })
  dataFilter.value.company = pk
}

const dataReset = () => {
  comStore.allDepartList = []
  comStore.company = null
  cashStore.comBankList = []
  cashStore.allComBankList = []
  cashStore.cashBookList = []
  cashStore.cashBookCount = 0
  dataFilter.value.company = null
}

onBeforeMount(() => {
  fetchBankCodeList()
  fetchAccSortList()
  fetchAllAccD1List()
  fetchAllAccD2List()
  fetchAllAccD3List()
  fetchFormAccD1List(null)
  fetchFormAccD2List(null, null)
  fetchFormAccD3List(null, null, null)

  dataSet(company.value || comStore.initComId)
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="CompanySelect"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddCash
        :company="company"
        @multi-submit="multiSubmit"
        @patchD3Hide="patchD3Hide"
        @onBankUpdate="onBankUpdate"
      />
      <TableTitleRow
        title="본사 입출금 관리"
        color="indigo"
        excel
        :url="excelUrl"
        :disabled="!company"
      />
      <CashList
        :company="company"
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @patchD3Hide="patchD3Hide"
        @onBankUpdate="onBankUpdate"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
