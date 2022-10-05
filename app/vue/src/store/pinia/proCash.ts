import api from '@/api'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import { AccountSort } from '@/store/types/comCash'
import {
  ProjectAccountD1,
  ProjectAccountD2,
  ProjectBankAccount,
  BalanceByAccount,
  ProjectCashBook,
  ProjectBudget,
  ExecAmountToBudget,
} from '@/store/types/proCash'
import { usePayment } from '@/store/pinia/payment'

export type CashBookFilter = {
  project?: number
  page?: number
  from_date?: string
  to_date?: string
  sort?: number | null
  pro_acc_d1?: number | null
  pro_acc_d2?: number | null
  bank_account?: number | null
  pay_order?: string
  pay_account?: string
  search?: string
}

export const useProCash = defineStore('proCash', () => {
  // state & getters
  const sortList = ref<AccountSort[]>([])

  const fetchProAccSortList = () =>
    api
      .get(`/project-acc-sort/`)
      .then(res => (sortList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const allAccD1List = ref<ProjectAccountD1[]>([])

  const fetchProAllAccD1List = () =>
    api
      .get(`/project-account-depth1/`)
      .then(res => (allAccD1List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const allAccD2List = ref<ProjectAccountD2[]>([])

  const fetchProAllAccD2List = () =>
    api
      .get(`/project-account-depth2/`)
      .then(res => (allAccD2List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const formAccD1List = ref<ProjectAccountD1[]>([])

  const fetchProFormAccD1List = (sort: number | null = null) => {
    const sortUri = sort ? `?projectaccountsort=${sort}` : ''
    api
      .get(`/project-account-depth1/${sortUri}`)
      .then(res => (formAccD1List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const formAccD2List = ref<ProjectAccountD2[]>([])

  const fetchProFormAccD2List = (
    d1: number | null = null,
    sort: number | null = null,
  ) => {
    const sortUri = sort
      ? `&d1__projectaccountsort=${sort}`
      : '&d1__projectaccountsort=1&d1__projectaccountsort=2&d1__projectaccountsort=3'
    return api
      .get(`/project-account-depth2/?d1=${d1 || ''}${sortUri}`)
      .then(res => (formAccD2List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const proBankAccountList = ref<ProjectBankAccount[]>([])

  const fetchProBankAccList = (project: number) =>
    api
      .get(`/project-bank-account/?project=${project}`)
      .then(res => (proBankAccountList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createProBankAcc = (payload: ProjectBankAccount) =>
    api
      .post(`/project-bank-account/`, payload)
      .then(res => fetchProBankAccList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const updateProBankAcc = (payload: ProjectBankAccount) =>
    api
      .put(`/project-bank-account/${payload.pk}/`, payload)
      .then(res => fetchProBankAccList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteProBankAcc = (pk: number, project: number) =>
    api
      .delete(`/project-bank-account/${pk}/`)
      .then(() =>
        fetchProBankAccList(project).then(() =>
          message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const balanceByAccList = ref<BalanceByAccount[]>([])

  const fetchBalanceByAccList = (payload: any) => {
    const { project, date } = payload
    let url = `/pr-balance-by-acc/?project=${project}`
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

  const proBudgetList = ref<ProjectBudget[]>([])

  const fetchProjectBudgetList = (project: number) =>
    api
      .get(`/budget/?project=${project}`)
      .then(res => (proBudgetList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const execAmountList = ref<ExecAmountToBudget[]>([])

  const fetchExecAmountList = (project: number, date = '') =>
    api
      .get(`/exec-amount/?project=${project}&date=${date}`)
      .then(res => (execAmountList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const proCashBookList = ref<ProjectCashBook[]>([])
  const proCashesCount = ref<number>(0)

  const fetchProjectCashList = (payload: CashBookFilter) => {
    const { project } = payload
    let url = `/project-cashbook/?project=${project}`
    if (payload.from_date) url += `&from_deal_date=${payload.from_date}`
    if (payload.to_date) url += `&to_deal_date=${payload.to_date}`
    if (payload.sort) url += `&sort=${payload.sort}`
    if (payload.pro_acc_d1) url += `&project_account_d1=${payload.pro_acc_d1}`
    if (payload.pro_acc_d2) url += `&project_account_d2=${payload.pro_acc_d2}`
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
              contract: res.data.contract,
              ordering: 'deal_date',
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
    api
      .patch(`/project-cashbook/${pk}/`, formData)
      .then(res => {
        fetchProjectCashList({
          project: res.data.project,
          ...filters,
        }).then(() => {
          paymentStore.fetchPaymentList({
            project: res.data.project,
            contract: res.data.contract,
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

  const deletePrCashBook = (
    payload: { pk: number; project: number; contract?: number | null } & {
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
            paymentStore.fetchPaymentList({ project, contract })
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
    if (payload.pro_acc_d1) url += `&project_account_d1=${payload.pro_acc_d1}`
    if (payload.pro_acc_d2) url += `&project_account_d2=${payload.pro_acc_d2}`
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
    proBankAccountList.value.filter(b => b.is_imprest),
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
            contract: res.data.contract,
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
            paymentStore.fetchPaymentList({ project, contract })
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

    allAccD1List,
    fetchProAllAccD1List,

    allAccD2List,
    fetchProAllAccD2List,

    formAccD1List,
    fetchProFormAccD1List,

    formAccD2List,
    fetchProFormAccD2List,

    proBankAccountList,
    fetchProBankAccList,
    createProBankAcc,
    updateProBankAcc,
    deleteProBankAcc,

    balanceByAccList,
    fetchBalanceByAccList,

    proDateCashBook,
    fetchDateCashBookList,

    proBudgetList,
    fetchProjectBudgetList,

    execAmountList,
    fetchExecAmountList,

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
  }
})
