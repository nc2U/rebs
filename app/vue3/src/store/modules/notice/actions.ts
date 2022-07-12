import api from '@/api'
import { FETCH_SALES_BILL_ISSUE } from '@/store/modules/notice/mutations-types'
import { errorHandle } from '@/utils/helper'

const actions = {
  fetchSalesBillIssue: ({ commit }: any, pk: number) => {
    return api
      .get(`/sales-bill-issue/${pk}/`)
      .then(res => {
        commit(FETCH_SALES_BILL_ISSUE, res.data)
      })
      .catch(err => errorHandle(err.response.data))
  },

  createSalesBillIssue: async ({ dispatch }: any, payload: any) => {
    try {
      return await api.post('/sales-bill-issue/', payload)
    } catch (err: any) {
      errorHandle(err.response.data)
    }
  },

  patchSalesBillIssue: async ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    try {
      await api.patch(`/sales-bill-issue/${pk}/`, formData)
    } catch (err: any) {
      errorHandle(err.response.data)
    }
  },

  updateSalesBillIssue: async ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    try {
      return await api.put(`/sales-bill-issue/${pk}/`, formData)
    } catch (err: any) {
      errorHandle(err.response.data)
    }
  },
}

export default actions
