import api from '@/api'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import { AccountSort } from '@/store/types/comCash'
import {
  ProjectAccountD2,
  ProjectAccountD3,
  ProBankAcc,
  BalanceByAccount,
  ProjectCashBook,
  CashBookFilter,
} from '@/store/types/proCash'
import { usePayment } from '@/store/pinia/payment'

export const useProCash = defineStore('proCash', () => {
  // state & getters
  const sortList = ref<AccountSort[]>([])

  const fetchProAccSortList = () =>
    api
      .get(`/project-acc-sort/`)
      .then(res => (sortList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const allAccD2List = ref<ProjectAccountD2[]>([])

  const fetchProAllAccD2List = () =>
    api
      .get(`/project-account-depth2/`)
      .then(res => (allAccD2List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const allAccD3List = ref<ProjectAccountD3[]>([])

  const fetchProAllAccD3List = () =>
    api
      .get(`/project-account-depth3/`)
      .then(res => (allAccD3List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const formAccD2List = ref<ProjectAccountD2[]>([])

  const fetchProFormAccD2List = (sort: number | null = null) => {
    const queryStr = sort ? `?d1__sorts=${sort}` : ''
    api
      .get(`/project-account-depth2/${queryStr}`)
      .then(res => (formAccD2List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const formAccD3List = ref<ProjectAccountD3[]>([])

  const fetchProFormAccD3List = (
    d2: number | null = null,
    sort: number | null = null,
  ) => {
    const uri = `?sort=${sort || ''}&d2=${d2 || ''}`
    return api
      .get(`/project-account-depth3/${uri}`)
      .then(res => (formAccD3List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const proBankAccountList = ref<ProBankAcc[]>([])
  const getProBanks = computed(() =>
    proBankAccountList.value.map(bk => ({
      value: bk.pk,
      label: bk.alias_name,
    })),
  )
  const allProBankAccountList = ref<ProBankAcc[]>([])

  const fetchProBankAccList = (project: number) =>
    api
      .get(
        `/project-bank-account/?project=${project}&is_hide=false&inactive=false`,
      )
      .then(res => (proBankAccountList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const fetchAllProBankAccList = (project: number) =>
    api
      .get(`/project-bank-account/?project=${project}`)
      .then(res => (allProBankAccountList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createProBankAcc = (payload: ProBankAcc) =>
    api
      .post(`/project-bank-account/`, payload)
      .then(res =>
        fetchAllProBankAccList(res.data.project).then(() =>
          fetchProBankAccList(res.data.project).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const updateProBankAcc = (payload: ProBankAcc) =>
    api
      .put(`/project-bank-account/${payload.pk}/`, payload)
      .then(res =>
        fetchAllProBankAccList(res.data.project).then(() =>
          fetchProBankAccList(res.data.project).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const patchProBankAcc = (payload: ProBankAcc) =>
    api
      .patch(`project-bank-account/${payload.pk}/`, payload)
      .then(res =>
        fetchAllProBankAccList(res.data.project).then(() =>
          fetchProBankAccList(res.data.project).then(() => message()),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const deleteProBankAcc = (pk: number, project: number) =>
    api
      .delete(`/project-bank-account/${pk}/`)
      .then(() =>
        fetchAllProBankAccList(project).then(() =>
          fetchProBankAccList(project).then(() =>
            message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.'),
          ),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const balanceByAccList = ref<BalanceByAccount[]>([])

  const fetchBalanceByAccList = (payload: {
    project: number
    direct?: string
    date?: string
  }) => {
    const { project, date, direct = '0' } = payload
    let url = `/pr-balance-by-acc/?project=${project}&bank_account__directpay=${direct}`
    if (date) url += `&date=${date}`
    return api
      .get(url)
      .then(res => (balanceByAccList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const proDateCashBook = ref<ProjectCashBook[]>([])

  const fetchDateCashBookList = (payload: {
    project: number
    date: string
  }) => {
    const { project, date } = payload
    const url = `/pr-date-cashbook/?project=${project}&date=${date}`
    return api
      .get(url)
      .then(res => (proDateCashBook.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const proCashBookList = ref<ProjectCashBook[]>([])
  const proCashesCount = ref<number>(0)

  const fetchProjectCashList = (payload: CashBookFilter) => {
    const { project } = payload
    let url = `/project-cashbook/?project=${project}`
    if (payload.from_date) url += `&from_deal_date=${payload.from_date}`
    if (payload.to_date) url += `&to_deal_date=${payload.to_date}`
    if (payload.sort) url += `&sort=${payload.sort}`
    if (payload.pro_acc_d2) url += `&project_account_d2=${payload.pro_acc_d2}`
    if (payload.pro_acc_d3) url += `&project_account_d3=${payload.pro_acc_d3}`
    if (payload.bank_account) url += `&bank_account=${payload.bank_account}`
    if (payload.search) url += `&search=${payload.search}`
    const page = payload.page ? payload.page : 1
    if (payload.page) url += `&page=${page}`
    return api
      .get(url)
      .then(res => {
        proCashBookList.value = res.data.results
        proCashesCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const proCashPages = (itemsPerPage: number) =>
    Math.ceil(proCashesCount.value / itemsPerPage)

  const paymentStore = usePayment()

  const createPrCashBook = (
    payload: ProjectCashBook & { sepData: ProjectCashBook | null } & {
      filters: CashBookFilter
    },
  ) => {
    const { filters, ...formData } = payload
    api
      .post(`/project-cashbook/`, formData)
      .then(res => {
        fetchProjectCashList({
          project: res.data.project,
          ...filters,
        }).then(() => {
          fetchProjectImprestList({
            project: res.data.project,
            ...filters,
          }).then(() => {
            paymentStore.fetchPaymentList({
              project: res.data.project,
              ...filters,
            })
            paymentStore.fetchAllPaymentList({
              project: res.data.project,
              contract: res.data.contract,
              ordering: 'deal_date',
            })
            message()
          })
        })
      })
      .catch(err => errorHandle(err.response.data))
  }

  const updatePrCashBook = (
    payload: ProjectCashBook & { sepData: ProjectCashBook | null } & {
      filters: CashBookFilter
    },
  ) => {
    const { pk, filters, ...formData } = payload
    api
      .put(`/project-cashbook/${pk}/`, formData)
      .then(res => {
        fetchProjectCashList({
          project: res.data.project,
          ...filters,
        }).then(() => {
          paymentStore.fetchPaymentList({
            project: res.data.project,
            ...filters,
          })
          paymentStore.fetchAllPaymentList({
            project: res.data.project,
            contract: res.data.contract,
            ordering: 'deal_date',
            ...filters,
          })
          message()
        })
      })
      .catch(err => errorHandle(err.response.data))
  }

  const patchPrCashBook = (
    payload: ProjectCashBook & { filters: CashBookFilter },
  ) => {
    const { pk, filters, ...formData } = payload
    return api
      .patch(`/project-cashbook/${pk}/`, formData)
      .then(res => {
        fetchProjectCashList({
          project: res.data.project,
          ...filters,
        }).then(() => {
          paymentStore.fetchPaymentList({
            project: res.data.project,
            ...filters,
          })
          paymentStore.fetchAllPaymentList({
            project: res.data.project,
            contract: res.data.contract,
            ordering: 'deal_date',
            ...filters,
          })
          message()
        })
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deletePrCashBook = (
    payload: {
      pk: number
      project: number
      contract?: number | null
    } & {
      filters?: CashBookFilter
    },
  ) => {
    const { pk, project, filters, contract } = payload

    api
      .delete(`/project-cashbook/${pk}/`)
      .then(() => {
        fetchProjectCashList({
          project,
          ...filters,
        }).then(() => {
          if (contract) {
            paymentStore.fetchPaymentList({
              project,
              ...filters,
            })
            paymentStore.fetchAllPaymentList({
              project,
              contract,
              ordering: 'deal_date',
            })
          }
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.')
        })
      })
      .catch(err => errorHandle(err.response.data))
  }

  const proImprestList = ref<ProjectCashBook[]>([])
  const proImprestCount = ref<number>(0)

  const fetchProjectImprestList = (payload: CashBookFilter) => {
    const { project } = payload
    let url = `/project-imprest/?project=${project}`
    if (payload.from_date) url += `&from_deal_date=${payload.from_date}`
    if (payload.to_date) url += `&to_deal_date=${payload.to_date}`
    if (payload.sort) url += `&sort=${payload.sort}`
    if (payload.pro_acc_d2) url += `&project_account_d2=${payload.pro_acc_d2}`
    if (payload.pro_acc_d3) url += `&project_account_d3=${payload.pro_acc_d3}`
    if (payload.bank_account) url += `&bank_account=${payload.bank_account}`
    if (payload.search) url += `&search=${payload.search}`
    const page = payload.page ? payload.page : 1
    if (payload.page) url += `&page=${page}`
    return api
      .get(url)
      .then(res => {
        proImprestList.value = res.data.results
        proImprestCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  const proImprestPages = (itemsPerPage: number) =>
    Math.ceil(proImprestCount.value / itemsPerPage)

  const imprestBAccount = computed(() =>
    allProBankAccountList.value.filter(b => b.is_imprest),
  )

  const getImpBankAccs = computed(() =>
    imprestBAccount.value.map(i => ({ value: i.pk, label: i.alias_name })),
  )

  const updatePrImprestBook = (
    payload: ProjectCashBook & { sepData: ProjectCashBook | null } & {
      filters: CashBookFilter
    },
  ) => {
    const { pk, filters, ...formData } = payload
    api
      .put(`/project-imprest/${pk}/`, formData)
      .then(res => {
        fetchProjectImprestList({
          project: res.data.project,
          ...filters,
        }).then(() => {
          paymentStore.fetchPaymentList({
            project: res.data.project,
            ...filters,
          })
          paymentStore.fetchAllPaymentList({
            project: res.data.project,
            contract: res.data.contract,
            ordering: 'deal_date',
          })
          message()
        })
      })
      .catch(err => errorHandle(err.response.data))
  }

  const patchPrImprestBook = (
    payload: ProjectCashBook & { filters: CashBookFilter },
  ) => {
    const { pk, filters, ...formData } = payload
    api
      .patch(`/project-imprest/${pk}/`, formData)
      .then(res => {
        fetchProjectImprestList({
          project: res.data.project,
          ...filters,
        }).then(() => {
          paymentStore.fetchPaymentList({
            project: res.data.project,
            ...filters,
          })
          paymentStore.fetchAllPaymentList({
            project: res.data.project,
            contract: res.data.contract,
            ordering: 'deal_date',
          })
          message()
        })
      })
      .catch(err => errorHandle(err.response.data))
  }

  const deletePrImprestBook = (
    payload: { pk: number; project: number; contract?: number | null } & {
      filters?: CashBookFilter
    },
  ) => {
    const { pk, project, filters, contract } = payload

    api
      .delete(`/project-imprest/${pk}/`)
      .then(() => {
        fetchProjectImprestList({
          project,
          ...filters,
        }).then(() => {
          if (contract) {
            paymentStore.fetchPaymentList({
              project,
              ...filters,
            })
            paymentStore.fetchAllPaymentList({
              project,
              contract,
              ordering: 'deal_date',
            })
          }
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.')
        })
      })
      .catch(err => errorHandle(err.response.data))
  }

  return {
    sortList,
    fetchProAccSortList,

    allAccD2List,
    fetchProAllAccD2List,

    allAccD3List,
    fetchProAllAccD3List,

    formAccD2List,
    fetchProFormAccD2List,

    formAccD3List,
    fetchProFormAccD3List,

    proBankAccountList,
    getProBanks,
    allProBankAccountList,
    fetchProBankAccList,
    fetchAllProBankAccList,
    createProBankAcc,
    updateProBankAcc,
    patchProBankAcc,
    deleteProBankAcc,

    balanceByAccList,
    fetchBalanceByAccList,

    proDateCashBook,
    fetchDateCashBookList,

    proCashBookList,
    proCashesCount,
    fetchProjectCashList,
    proCashPages,
    createPrCashBook,
    updatePrCashBook,
    patchPrCashBook,
    deletePrCashBook,

    proImprestList,
    proImprestCount,
    fetchProjectImprestList,
    proImprestPages,
    updatePrImprestBook,
    patchPrImprestBook,
    deletePrImprestBook,
    imprestBAccount,
    getImpBankAccs,
  }
})
