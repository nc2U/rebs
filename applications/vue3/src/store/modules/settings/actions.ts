import api from '@/api'
import {
  FETCH_COMPANY,
  FETCH_COMPANY_LIST,
} from '@/store/modules/settings/mutations-types'
import { message } from '@/utils/helper'

const actions = {
  fetchCompanyList: ({ commit }: any) => {
    api
      .get('/company/')
      .then((res) => {
        commit(FETCH_COMPANY_LIST, res.data.results)
      })
      .catch((err) => console.log(err))
  },

  fetchCompany: ({ commit }: any, id: { id: string }) => {
    api
      .get(`/company/${id}/`)
      .then((res) => {
        commit(FETCH_COMPANY, res.data)
      })
      .catch((err) => console.log(err))
  },

  createCompany: ({ dispatch }: any, payload: any) => {
    api
      .post('/company/', payload)
      .then((res) => {
        dispatch('fetchCompany', res.data.id)
        dispatch('fetchCompanyList')
        message()
      })
      .catch((err) => alert(err.response.data.detail))
  },

  updateCompany: ({ dispatch }: any, payload: any) => {
    api
      .put(`/company/${payload.id}/`, payload)
      .then((res) => {
        dispatch('fetchCompany', res.data.id)
        dispatch('fetchCompanyList')
        message()
      })
      .catch((err) => alert(err.response.data.detail))
  },
}

export default actions
