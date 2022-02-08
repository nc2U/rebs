import api from '@/api'
import { FETCH_ORDER_GROUP_LIST } from '@/store/modules/contract/mutations-types'

const actions = {
  fetchOrderGroupList: ({ commit }: any, pk?: number) => {
    api
      .get(`/order-group/?project=${pk}`)
      .then(res => {
        commit(FETCH_ORDER_GROUP_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  createOrderGroup: ({ dispatch }: any, payload: any) => {
    api
      .post(`/order-group/`, payload)
      .then(res => {
        dispatch('fetchOrderGroupList', res.data.project)
      })
      .catch(err => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },

  updateProject: ({ dispatch }: any, payload: any) => {
    api
      .put(`/order-group/${payload.id}/`, payload)
      .then(res => {
        dispatch('fetchOrderGroupList', res.data.project)
      })
      .catch(err => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },

  deleteProject: ({ dispatch }: any, pk: any) => {
    api.delete(`/order-group/${pk}/`).then(() => {
      dispatch('fetchOrderGroupList', 1)
    })
  },
}

export default actions
