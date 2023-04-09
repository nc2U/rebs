<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
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

const companyStore = useCompany()
const initComId = computed(() => companyStore.initComId)
const company = computed(() => companyStore.company?.pk)

const fetchCompany = (pk: number) => companyStore.fetchCompany(pk)
const fetchAllDepartList = (com: number) => companyStore.fetchAllDepartList(com)

const comCashStore = useComCash()
const fetchBankCodeList = () => comCashStore.fetchBankCodeList()
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
const fetchAllComBankAccList = (pk: number) =>
  comCashStore.fetchAllComBankAccList(pk)
const patchComBankAcc = (payload: CompanyBank) =>
  comCashStore.patchComBankAcc(payload)

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
    fetchAllDepartList(target)
    fetchComBankAccList(target)
    fetchAllComBankAccList(target)
    fetchCashBookList({ company: target })
  } else {
    companyStore.allDepartList = []
    companyStore.company = null
    comCashStore.comBankList = []
    comCashStore.allComBankList = []
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

onBeforeMount(() => {
  fetchBankCodeList()
  fetchAccSortList()
  fetchAllAccD1List()
  fetchAllAccD2List()
  fetchAllAccD3List()
  fetchFormAccD1List(null)
  fetchFormAccD2List(null, null)
  fetchFormAccD3List(null, null, null)
  if (initComId.value) {
    fetchCompany(initComId.value)
    fetchAllDepartList(initComId.value)
    fetchComBankAccList(initComId.value)
    fetchAllComBankAccList(initComId.value)
    fetchCashBookList({ company: initComId.value })
    dataFilter.value.company = initComId.value
  }
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
