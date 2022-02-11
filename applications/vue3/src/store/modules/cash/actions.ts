import api from '@/api'
import {
  FETCH_PRICE_LIST,
  FETCH_PAY_ORDER_LIST,
} from '@/store/modules/cash/mutations-types'
import { message } from '@/utils/helper'

const actions = {
  fetchPriceList: ({ commit }: any, payload: any) => {
    const { project, order_group, unit_type } = payload
    api
      .get(
        `/price/?project=${project}&order_group=${order_group}&unit_type=${unit_type}`,
      )
      .then(res => {
        commit(FETCH_PRICE_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  createPrice: ({ dispatch }: any, payload: any) => {
    api
      .post(`/price/`, payload)
      .then(() => {
        const { project, order_group, unit_type } = payload
        dispatch('fetchPriceList', { project, order_group, unit_type })
        message()
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

  updatePrice: ({ dispatch }: any, payload: any) => {
    const { pk } = payload
    delete payload.pk
    api
      .put(`/price/${pk}/`, payload)
      .then(() => {
        const { project, order_group, unit_type } = payload
        dispatch('fetchPriceList', { project, order_group, unit_type })
        message()
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

  deletePrice: ({ dispatch }: any, payload: any) => {
    const { pk, projId } = payload
    api
      .delete(`/price/${pk}/`)
      .then(() => {
        dispatch('fetchPriceList', projId)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
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

  fetchPayOrderList: ({ commit }: any, pk: any) => {
    api
      .get(`/pay-order/?project=${pk}`)
      .then(res => {
        commit(FETCH_PAY_ORDER_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  createPayOrder: ({ dispatch }: any, payload: any) => {
    api
      .post(`/pay-order/`, payload)
      .then(res => {
        dispatch('fetchPayOrderList', res.data.project)
        message()
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

  updatePayOrder: ({ dispatch }: any, payload: any) => {
    const { pk } = payload
    delete payload.pk
    api
      .put(`/pay-order/${pk}/`, payload)
      .then(() => {
        const { project } = payload
        dispatch('fetchPayOrderList', { project })
        message()
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

  deletePayOrder: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/pay-order/${pk}/`)
      .then(() => {
        dispatch('fetchPayOrderList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
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
}

export default actions
