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
        commit(FETCH_COMPANY_LIST, res.data)
      })
      .catch((err) => console.log(err))
  },

  fetchCompany: ({ commit }: any, pk: { pk: string }) => {
    api
      .get(`/company/${pk}/`)
      .then((res) => {
        commit(FETCH_COMPANY, res.data)
      })
      .catch((err) => console.log(err))
  },

  createCompany: ({ dispatch }: any, payload: any) => {
    api
      .post('/company/', payload)
      .then((res) => {
        dispatch('fetchCompany', res.data.pk)
        dispatch('fetchCompanyList')
        message()
      })
      .catch((err) => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },

  updateCompany: ({ dispatch }: any, payload: any) => {
    api
      .put(`/company/${payload.pk}/`, payload)
      .then((res) => {
        dispatch('fetchCompany', res.data.pk)
        dispatch('fetchCompanyList')
        message()
      })
      .catch((err) => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },
}

export default actions
