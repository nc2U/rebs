import api from '@/api'
import {
  FETCH_COM_ACC_D1_LIST,
  FETCH_COM_ACC_D2_LIST,
  FETCH_COM_ACC_D3_LIST,
  FETCH_COMPAY_BANK_LIST,
  FETCH_CASHBOOK_LIST,
} from '@/store/modules/comCash/mutations-types'
import { message } from '@/utils/helper'

const actions = {
  fetchAccountD1List: ({ commit }: any) => {
    api
      .get(`/account-depth1/`)
      .then(res => {
        commit(FETCH_COM_ACC_D1_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchAccountD2List: ({ commit }: any) => {
    api
      .get(`/account-depth2/`)
      .then(res => {
        commit(FETCH_COM_ACC_D2_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchAccountD3List: ({ commit }: any) => {
    api
      .get(`/account-depth3/`)
      .then(res => {
        commit(FETCH_COM_ACC_D3_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchCompanyBankAccountList: ({ commit }: any, company: any) => {
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
        dispatch('fetchCompanyBankAccountList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  updateCompanyBankAccount: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/company-bank-account/${pk}/`, formData)
      .then(res => {
        dispatch('fetchCompanyBankAccountList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  deleteCompanyBankAccount: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/company-bank-account/${pk}/`)
      .then(() => {
        dispatch('fetchCompanyBankAccountList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => console.log(err.response.data))
  },

  fetchCashBookList: ({ commit }: any, payload: any) => {
    const { company } = payload
    let url = `/cashbook/?company=${company}`
    if (payload.from_date) url += `&from_deal_date=${payload.from_date}`
    if (payload.to_date) url += `&to_deal_date=${payload.to_date}`
    // if (payload.sort) url += `&cash_category1=${payload.sort}`
    // if (payload.accountD1) url += `&project_account_d1=${payload.accountD1}`
    // if (payload.accountD2) url += `&project_account_d2=${payload.accountD2}`
    // if (payload.bank_account) url += `&bank_account=${payload.bank_account}`
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
        dispatch('fetchCashBookList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  updateCashBook: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/cashbook/${pk}/`, formData)
      .then(res => {
        dispatch('fetchCashBookList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  deleteCashBook: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/cashbook/${pk}/`)
      .then(() => {
        dispatch('fetchCashBookList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => console.log(err.response.data))
  },
}

export default actions
