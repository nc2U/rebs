import api from '@/api'
import {
  FETCH_ACC_D1_LIST,
  FETCH_ACC_D2_LIST,
  FETCH_ACC_D3_LIST,
  FETCH_FORM_ACC_D1_LIST,
  FETCH_FORM_ACC_D2_LIST,
  FETCH_FORM_ACC_D3_LIST,
  FETCH_COMPAY_BANK_LIST,
  FETCH_CASHBOOK_LIST,
  FETCH_ACC_SORT_LIST,
} from '@/store/modules/comCash/mutations-types'
import { message } from '@/utils/helper'

const actions = {
  fetchAccSortList: ({ commit }: any) => {
    api
      .get(`/account-sort/`)
      .then(res => {
        commit(FETCH_ACC_SORT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchAllAccD1List: ({ commit }: any) => {
    const url = `/account-depth1/`
    api
      .get(url)
      .then(res => {
        commit(FETCH_ACC_D1_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchAllAccD2List: ({ commit }: any) => {
    const url = `/account-depth2/`
    api
      .get(url)
      .then(res => {
        commit(FETCH_ACC_D2_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchAllAccD3List: ({ commit }: any) => {
    const url = `/account-depth3/`
    api
      .get(url)
      .then(res => {
        commit(FETCH_ACC_D3_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchFormAccD1List: ({ commit }: any, data?: any) => {
    let url = `/account-depth1/`
    const sort = data && data.sort ? data.sort : ''
    if (sort) url += `?accountsort=${sort}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_FORM_ACC_D1_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchFormAccD2List: ({ commit }: any, data?: any) => {
    const sort = data && data.sort ? data.sort : ''
    const d1 = data && data.d1 ? data.d1 : ''
    let url = `/account-depth2/?d1=${d1}`
    if (sort) url += `&d1__accountsort=${sort}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_FORM_ACC_D2_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchFormAccD3List: ({ commit }: any, data?: any) => {
    const sort = data && data.sort ? data.sort : ''
    const d1 = data && data.d1 ? data.d1 : ''
    const d2 = data && data.d2 ? data.d2 : ''
    let url = `/account-depth3/?d2__d1=${d1}&d2=${d2}`
    if (sort) url += `&d2__d1__accountsort=${sort}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_FORM_ACC_D3_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchComBankAccList: ({ commit }: any, company: any) => {
    api
      .get(`/company-bank-account/?company=${company}`)
      .then(res => {
        commit(FETCH_COMPAY_BANK_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  createCompanyBankAccount: ({ dispatch }: any, payload: any) => {
    api
      .post(`/company-bank-account/`, payload)
      .then(res => {
        dispatch('fetchComBankAccList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  updateCompanyBankAccount: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/company-bank-account/${pk}/`, formData)
      .then(res => {
        dispatch('fetchComBankAccList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  deleteCompanyBankAccount: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/company-bank-account/${pk}/`)
      .then(() => {
        dispatch('fetchComBankAccList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => console.log(err.response.data))
  },

  fetchCashBookList: ({ commit }: any, payload: any) => {
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
    api
      .get(url)
      .then(res => {
        commit(FETCH_CASHBOOK_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  createCashBook: ({ dispatch }: any, payload: any) => {
    api
      .post(`/cashbook/`, payload)
      .then(res => {
        dispatch('fetchCashBookList', { company: res.data.company })
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  updateCashBook: ({ dispatch }: any, payload: any) => {
    const { pk, page, search, ...formData } = payload
    api
      .put(`/cashbook/${pk}/`, formData)
      .then(res => {
        dispatch('fetchCashBookList', {
          company: res.data.company,
          page,
          search,
        })
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  deleteCashBook: ({ dispatch }: any, payload: any) => {
    const { pk, page, company } = payload
    api
      .delete(`/cashbook/${pk}/`)
      .then(() => {
        dispatch('fetchCashBookList', { company, page })
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => console.log(err.response.data))
  },
}

export default actions
