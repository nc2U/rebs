import api from '@/api'
import {
  FETCH_ORDER_GROUP,
  FETCH_ORDER_GROUP_LIST,
} from '@/store/modules/contract/mutations-types'

const actions = {
  fetchOrderGroupList: ({ commit }: any) => {
    api
      .get('/order-group/')
      .then((res) => {
        commit(FETCH_ORDER_GROUP_LIST, res.data.results)
      })
      .catch((err) => console.log(err))
  },

  fetchOrderGroup: ({ commit }: any, id: { id: string }) => {
    api
      .get(`/order-group/${id}/`)
      .then((res) => {
        commit(FETCH_ORDER_GROUP, res.data)
      })
      .catch((err) => console.log(err))
  },

  createOrderGroup: ({ dispatch }: any, payload: any) => {
    api
      .post(`/order-group/`, payload)
      .then((res) => {
        dispatch('fetchOrderGroup', res.data.id)
        dispatch('fetchOrderGroupList')
      })
      .catch((err) => alert(err.response.data.detail))
  },

  updateProject: ({ dispatch }: any, payload: any) => {
    api
      .put(`/order-group/${payload.id}/`, payload)
      .then((res) => {
        dispatch('fetchOrderGroup', res.data.id)
        dispatch('fetchOrderGroupList')
      })
      .catch((err) => alert(err.response.data.detail))
  },

  deleteProject: ({ dispatch }: any, id: any) => {
    api.delete(`/order-group/${id}/`).then((res) => {
      console.log(res.data)
      dispatch('fetchOrderGroupList')
    })
  },
}

export default actions
