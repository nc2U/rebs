import api from '@/api'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { errorHandle, message } from '@/utils/helper'
import {
  BankCode,
  AccountSort,
  AccountD1,
  AccountD2,
  AccountD3,
  CompanyBank,
  BalanceByAccount,
  CashBook,
  SepItems,
} from '@/store/types/comCash'

export type DataFilter = {
  page?: number
  company?: number | null
  from_date?: string
  to_date?: string
  sort?: number | null
  account_d1?: number | null
  account_d2?: number | null
  account_d3?: number | null
  bank_account?: number | null
  search?: string
}

export const useComCash = defineStore('comCash', () => {
  // state & getters
  const bankCodeList = ref<BankCode[]>([])

  const fetchBankCodeList = () =>
    api
      .get('/bank-code/')
      .then(res => (bankCodeList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const sortList = ref<AccountSort[]>([])

  const fetchAccSortList = () =>
    api
      .get(`/account-sort/`)
      .then(res => (sortList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const listAccD1List = ref<AccountD1[]>([])

  const fetchAllAccD1List = () =>
    api
      .get(`/account-depth1/`)
      .then(res => (listAccD1List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const listAccD2List = ref<AccountD2[]>([])

  const fetchAllAccD2List = () =>
    api
      .get(`/account-depth2/`)
      .then(res => (listAccD2List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const listAccD3List = ref<AccountD3[]>([])

  const fetchAllAccD3List = () =>
    api
      .get(`/account-depth3/`)
      .then(res => (listAccD3List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const patchAccD3 = (payload: { pk: number; is_hide: boolean }) => {
    const { pk, ...hideData } = payload
    return api
      .patch(`/account-depth3/${pk}/`, hideData)
      .then(() => {
        fetchAllAccD3List().then(() =>
          fetchFormAccD3List(null, null, null).then(() => message()),
        )
      })
      .catch(err => errorHandle(err.response.data))
  }

  const formAccD1List = ref<AccountD1[]>([])

  const fetchFormAccD1List = (sort: number | null) => {
    const uSort = sort ? `?accountsort=${sort}` : ''
    return api
      .get(`/account-depth1/${uSort}`)
      .then(res => (formAccD1List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const formAccD2List = ref<AccountD2[]>([])

  const fetchFormAccD2List = (sort: number | null, d1: number | null) => {
    const uSort = sort ? `d1__accountsort=${sort}` : ''
    const uD1 = d1 ? `&d1=${d1}` : ''
    return api
      .get(`/account-depth2/?${uSort}${uD1}`)
      .then(res => (formAccD2List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const formAccD3List = ref<AccountD3[]>([])

  const fetchFormAccD3List = (
    sort: number | null,
    d1: number | null,
    d2: number | null,
  ) => {
    const uSort = sort ? `d2__d1__accountsort=${sort}` : ''
    const uD1 = d1 ? `&d2__d1=${d1}` : ''
    const uD2 = d2 ? `&d2=${d2}` : ''
    return api
      .get(`/account-depth3/?${uSort}${uD1}${uD2}&is_hide=false`)
      .then(res => (formAccD3List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const comBankList = ref<CompanyBank[]>([])
  const allComBankList = ref<CompanyBank[]>([])

  const fetchComBankAccList = (company: number) =>
    api
      .get(
        `/company-bank-account/?company=${company}&is_hide=false&inactive=false`,
      )
      .then(res => (comBankList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const fetchAllComBankAccList = (company: number) =>
    api
      .get(`/company-bank-account/?company=${company}`)
      .then(res => (allComBankList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createCompanyBankAccount = (payload: CompanyBank) =>
    api
      .post(`/company-bank-account/`, payload)
      .then(res =>
        fetchAllComBankAccList(res.data.company).then(() =>
          fetchComBankAccList(res.data.company).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateCompanyBankAccount = (payload: CompanyBank) =>
    api
      .put(`/company-bank-account/${payload.pk}/`, payload)
      .then(res =>
        fetchAllComBankAccList(res.data.company).then(() =>
          fetchComBankAccList(res.data.company).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const patchComBankAcc = (payload: CompanyBank) =>
    api
      .patch(`company-bank-account/${payload.pk}/`, payload)
      .then(res =>
        fetchAllComBankAccList(res.data.company).then(() =>
          fetchComBankAccList(res.data.company).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const deleteCompanyBankAccount = (pk: number, company: number) =>
    api
      .delete(`/company-bank-account/${pk}/`)
      .then(() =>
        fetchAllComBankAccList(company).then(() =>
          fetchComBankAccList(company).then(() =>
            message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.'),
          ),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const comBalanceByAccList = ref<BalanceByAccount[]>([])

  const fetchComBalanceByAccList = (payload: {
    company: number
    date: string
  }) => {
    const { company, date } = payload
    const dateUri = date ? `&date=${date}` : ''
    return api
      .get(`/balance-by-acc/?company=${company}${dateUri}`)
      .then(res => (comBalanceByAccList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const dateCashBook = ref<CashBook[]>([])

  const fetchDateCashBookList = (payload: {
    company: number
    date: string
  }) => {
    const { company, date } = payload
    return api
      .get(`/date-cashbook/?company=${company}&date=${date}`)
      .then(res => (dateCashBook.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const cashBookList = ref<CashBook[]>([])
  const getCashLogs = computed(() =>
    cashBookList.value
      ? cashBookList.value.map((c: CashBook) => ({
          pk: c.pk,
          company: c.company,
          deal_date: c.deal_date,
          sort: c.sort,
          sort_desc: c.sort
            ? sortList.value
                .filter(sort => sort.pk === c.sort)
                .map(sort => sort.name)[0]
            : '',
          account_d1: c.account_d1,
          account_d1_desc: c.account_d1
            ? listAccD1List.value
                .filter(d1 => d1.pk === c.account_d1)
                .map(d1 => d1.name)[0]
            : '',
          account_d2: c.account_d2,
          account_d3: c.account_d3,
          account_d3_desc: c.account_d3
            ? listAccD3List.value
                .filter(d3 => d3.pk === c.account_d3)
                .map(d3 => d3.name)[0]
            : '',
          is_separate: c.is_separate,
          separated: c.separated,
          sepItems: c.sepItems,
          content: c.content,
          trader: c.trader,
          bank_account: c.bank_account,
          bank_account_desc: comBankList.value
            ? comBankList.value
                .filter((b: CompanyBank) => b.pk === c.bank_account)
                .map((b: CompanyBank) => b.alias_name)[0]
            : [],
          income: c.income,
          outlay: c.outlay,
          evidence: c.evidence,
          evidence_desc: c.evidence_desc,
          note: c.note,
        }))
      : [],
  )
  const cashBookCount = ref<number>(0)

  const cashesPages = (itemsPerPage: number) =>
    Math.ceil(cashBookCount.value / itemsPerPage)

  const fetchCashBookList = (payload: DataFilter) => {
    const { company } = payload
    let url = `/cashbook/?company=${company}`
    if (payload.from_date) url += `&from_deal_date=${payload.from_date}`
    if (payload.to_date) url += `&to_deal_date=${payload.to_date}`
    if (payload.sort) url += `&sort=${payload.sort}`
    if (payload.account_d1) url += `&account_d1=${payload.account_d1}`
    if (payload.account_d2) url += `&account_d2=${payload.account_d2}`
    if (payload.account_d3) url += `&account_d3=${payload.account_d3}`
    if (payload.bank_account) url += `&bank_account=${payload.bank_account}`
    if (payload.search) url += `&search=${payload.search}`
    const page = payload.page ? payload.page : 1
    if (payload.page) url += `&page=${page}`

    return api
      .get(url)
      .then(res => {
        cashBookList.value = res.data.results
        cashBookCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const createCashBook = (payload: CashBook & { sepData: SepItems | null }) =>
    api
      .post(`/cashbook/`, payload)
      .then(res =>
        fetchCashBookList({ company: res.data.company }).then(() => message()),
      )
      .catch(err => errorHandle(err.response.data))

  const updateCashBook = (
    payload: CashBook & { sepData: SepItems | null } & { filters: DataFilter },
  ) => {
    const { filters, ...formData } = payload
    return api
      .put(`/cashbook/${formData.pk}/`, formData)
      .then(res =>
        fetchCashBookList({
          company: res.data.company,
          ...filters,
        }).then(() => message()),
      )
      .catch(err => errorHandle(err.response.data))
  }

  const deleteCashBook = (payload: CashBook & { filters: DataFilter }) => {
    const { pk, filters, company } = payload
    return api
      .delete(`/cashbook/${pk}/`)
      .then(() =>
        fetchCashBookList({ company, ...filters }).then(() =>
          message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))
  }

  return {
    bankCodeList,
    fetchBankCodeList,

    sortList,
    fetchAccSortList,

    formAccD1List,
    fetchAllAccD1List,
    formAccD2List,
    fetchAllAccD2List,
    formAccD3List,
    fetchAllAccD3List,
    patchAccD3,

    listAccD1List,
    fetchFormAccD1List,
    listAccD2List,
    fetchFormAccD2List,
    listAccD3List,
    fetchFormAccD3List,

    comBankList,
    allComBankList,
    fetchComBankAccList,
    fetchAllComBankAccList,
    createCompanyBankAccount,
    updateCompanyBankAccount,
    patchComBankAcc,
    deleteCompanyBankAccount,

    comBalanceByAccList,
    fetchComBalanceByAccList,

    dateCashBook,
    fetchDateCashBookList,

    cashBookList,
    getCashLogs,
    cashBookCount,
    cashesPages,
    fetchCashBookList,
    createCashBook,
    updateCashBook,
    deleteCashBook,
  }
})
