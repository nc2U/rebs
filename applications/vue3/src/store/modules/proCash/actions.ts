import api from '@/api'
import {
  FETCH_ACCOUNT_D1_LIST,
  FETCH_ACCOUNT_D2_LIST,
  FETCH_P_BANK_ACCOUNT_LIST,
  FETCH_P_CASHBOOK_LIST,
} from '@/store/modules/proCash/mutations-types'
import { message } from '@/utils/helper'

const actions = {
  fetchProAccountD1List: ({ commit }: any) => {
    api
      .get(`/project-account-depth1/`)
      .then(res => {
        commit(FETCH_ACCOUNT_D1_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProAccountD2List: ({ commit }: any, d1?: string) => {
    const url = d1
      ? `/project-account-depth2/?d1=${d1}`
      : `/project-account-depth2/`
    api
      .get(url)
      .then(res => {
        commit(FETCH_ACCOUNT_D2_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProjectBankAccountList: ({ commit }: any, project: any) => {
    api
      .get(`/project-bank-account/?project=${project}`)
      .then(res => {
        commit(FETCH_P_BANK_ACCOUNT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  createProjectBankAccount: ({ dispatch }: any, payload: any) => {
    api
      .post(`/project-bank-account/`, payload)
      .then(res => {
        dispatch('fetchProjectBankAccountList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  updateProjectBankAccount: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/project-bank-account/${pk}/`, formData)
      .then(res => {
        dispatch('fetchProjectBankAccountList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  deleteProjectBankAccount: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/project-bank-account/${pk}/`)
      .then(() => {
        dispatch('fetchProjectBankAccountList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProjectCashList: ({ commit }: any, payload: any) => {
    const { project } = payload
    let url = `/project-cashbook/?project=${project}`
    const page = payload.page ? payload.page : 1
    if (payload.page) url += `&page=${page}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_P_CASHBOOK_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  createPrCashBook: ({ dispatch }: any, payload: any) => {
    api
      .post(`/project-cashbook/`, payload)
      .then(res => {
        dispatch('fetchProjectCashList', res.data.project)
        dispatch('fetchPaymentList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  updatePrCashBook: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/project-cashbook/${pk}/`, formData)
      .then(res => {
        dispatch('fetchProjectCashList', res.data.project)
        dispatch('fetchPaymentList', res.data.project)
        message()
      })
      .catch(err => console.log(err.response.data))
  },

  deletePrCashBook: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/project-cashbook/${pk}/`)
      .then(() => {
        dispatch('fetchProjectCashList', project)
        dispatch('fetchPaymentList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => console.log(err.response.data))
  },
}

export default actions
