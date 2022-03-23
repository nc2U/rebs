import api from '@/api'
import {
  FETCH_P_ACC_SORT_LIST,
  FETCH_ALL_ACC_D1_LIST,
  FETCH_ALL_ACC_D2_LIST,
  FETCH_FORM_ACC_D1_LIST,
  FETCH_FORM_ACC_D2_LIST,
  FETCH_P_BANK_ACCOUNT_LIST,
  FETCH_P_DATE_CASHBOOK,
  FETCH_P_CASHBOOK_LIST,
  FETCH_P_IMPREST_LIST,
  FETCH_BALANCE_BY_ACC_LIST,
  FETCH_P_BUDGET_LIST,
  FETCH_EXEC_AMOUNT_LIST,
} from '@/store/modules/proCash/mutations-types'
import { message } from '@/utils/helper'

const actions = {
  fetchProAccSortList: ({ commit }: any) => {
    api
      .get(`/project-acc-sort/`)
      .then(res => {
        commit(FETCH_P_ACC_SORT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProAllAccD1List: ({ commit }: any) => {
    api
      .get(`/project-account-depth1/`)
      .then(res => {
        commit(FETCH_ALL_ACC_D1_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProAllAccD2List: ({ commit }: any) => {
    api
      .get(`/project-account-depth2/`)
      .then(res => {
        commit(FETCH_ALL_ACC_D2_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProFormAccD1List: ({ commit }: any, sort?: string) => {
    const url = sort
      ? `/project-account-depth1/?projectaccountsort=${sort}`
      : `/project-account-depth1/`
    api
      .get(url)
      .then(res => {
        commit(FETCH_FORM_ACC_D1_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProFormAccD2List: ({ commit }: any, payload?: any) => {
    const d1 = payload && payload.d1 ? payload.d1 : ''
    let url = `/project-account-depth2/?d1=${d1}`
    const sort =
      payload && payload.sort
        ? `&d1__projectaccountsort=${payload.sort}`
        : '&d1__projectaccountsort=1&d1__projectaccountsort=2&d1__projectaccountsort=3'
    url = `${url}${sort}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_FORM_ACC_D2_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProBankAccList: ({ commit }: any, project: any) => {
    api
      .get(`/project-bank-account/?project=${project}`)
      .then(res => {
        commit(FETCH_P_BANK_ACCOUNT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  createProBankAcc: ({ dispatch }: any, payload: any) => {
    api
      .post(`/project-bank-account/`, payload)
      .then(res => {
        dispatch('fetchProBankAccList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  updateProBankAcc: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/project-bank-account/${pk}/`, formData)
      .then(res => {
        dispatch('fetchProBankAccList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  deleteProBankAcc: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/project-bank-account/${pk}/`)
      .then(() => {
        dispatch('fetchProBankAccList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => console.log(err.response.data))
  },

  fetchBalanceByAccList: ({ commit }: any, payload: any) => {
    const { project, date } = payload
    let url = `/pcash-by-acc/?project=${project}`
    if (date) url += `&date=${date}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_BALANCE_BY_ACC_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchDateCashBookList: ({ commit }: any, payload: any) => {
    const { project, date } = payload
    const url = `/pr-date-cashbook/?project=${project}&date=${date}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_P_DATE_CASHBOOK, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProjectBudgetList: ({ commit }: any, pk: number) => {
    api
      .get(`/budget/?project=${pk}`)
      .then(res => {
        commit(FETCH_P_BUDGET_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchExecAmountList: ({ commit }: any, payload: any) => {
    const { project, date } = payload
    let url = `/exec-amount/?project=${project}`
    if (date) url += `&date=${date}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_EXEC_AMOUNT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProjectCashList: ({ commit }: any, payload: any) => {
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
    api
      .get(url)
      .then(res => {
        commit(FETCH_P_CASHBOOK_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProjectImprestList: ({ commit }: any, payload: any) => {
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
    api
      .get(url)
      .then(res => {
        commit(FETCH_P_IMPREST_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  createPrCashBook: ({ dispatch }: any, payload: any) => {
    const { filters, ...formData } = payload
    api
      .post(`/project-cashbook/`, formData)
      .then(res => {
        dispatch('fetchProjectCashList', {
          project: res.data.project,
          ...filters,
        })
        dispatch('fetchProjectImprestList', {
          project: res.data.project,
          ...filters,
        })
        dispatch(
          'payment/fetchPaymentList',
          {
            project: res.data.project,
            contract: res.data.contract,
            ordering: 'deal_date',
          },
          { root: true },
        )
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  updatePrCashBook: ({ dispatch }: any, payload: any) => {
    const { pk, filters, ...formData } = payload
    api
      .put(`/project-cashbook/${pk}/`, formData)
      .then(res => {
        dispatch('fetchProjectCashList', {
          project: res.data.project,
          ...filters,
        })
        dispatch('fetchProjectImprestList', {
          project: res.data.project,
          ...filters,
        })
        dispatch(
          'payment/fetchPaymentList',
          {
            project: res.data.project,
            ...filters,
          },
          { root: true },
        )
        dispatch(
          'payment/fetchAllPaymentList',
          {
            project: res.data.project,
            contract: res.data.contract,
            ordering: 'deal_date',
          },
          { root: true },
        )
        message()
      })
      .catch(err => console.log(err.response.data))
  },
  patchPrCashBook: ({ dispatch }: any, payload: any) => {
    const { pk, filters, ...formData } = payload
    api
      .patch(`/project-cashbook/${pk}/`, formData)
      .then(res => {
        dispatch('fetchProjectCashList', {
          project: res.data.project,
          ...filters,
        })
        dispatch('fetchProjectImprestList', {
          project: res.data.project,
          ...filters,
        })
        dispatch(
          'payment/fetchPaymentList',
          {
            project: res.data.project,
            contract: res.data.contract,
          },
          { root: true },
        )
        dispatch(
          'payment/fetchAllPaymentList',
          {
            project: res.data.project,
            contract: res.data.contract,
            ordering: 'deal_date',
          },
          { root: true },
        )
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  deletePrCashBook: ({ dispatch }: any, payload: any) => {
    const { pk, project, filters, contract } = payload

    api
      .delete(`/project-cashbook/${pk}/`)
      .then(() => {
        dispatch('fetchProjectCashList', {
          project,
          ...filters,
        })
        dispatch('fetchProjectImprestList', {
          project,
          ...filters,
        })
        dispatch(
          'payment/fetchPaymentList',
          { project, contract },
          { root: true },
        )
        dispatch(
          'payment/fetchAllPaymentList',
          { project, contract, ordering: 'deal_date' },
          { root: true },
        )
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => console.log(err.response.data))
  },
}

export default actions
