import api from '@/api'
import {
  FETCH_PRICE_LIST,
  FETCH_PAY_ORDER_LIST,
  FETCH_DWON_PAYMENT,
  FETCH_PAYMENT_LIST,
  FETCH_PAYMENT_SUM_LIST,
  FETCH_CONTRACT_NUM_LIST,
} from '@/store/modules/payment/mutations-types'
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
      .catch(err => console.log(err.response.data))
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
    const { pk, ...formData } = payload
    api
      .put(`/price/${pk}/`, formData)
      .then(() => {
        const { project, order_group, unit_type } = formData
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
    const { pk, ...formData } = payload
    api
      .delete(`/price/${pk}/`)
      .then(() => {
        const { project, order_group, unit_type } = formData
        dispatch('fetchPriceList', { project, order_group, unit_type })
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
      .catch(err => console.log(err.response.data))
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
    const { pk, ...formData } = payload
    api
      .put(`/pay-order/${pk}/`, formData)
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

  fetchDownPayList: ({ commit }: any, pk: any) => {
    api
      .get(`/down-payment/?project=${pk}`)
      .then(res => {
        commit(FETCH_DWON_PAYMENT, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  createDownPay: ({ dispatch }: any, payload: any) => {
    api
      .post(`/down-payment/`, payload)
      .then(res => {
        dispatch('fetchDownPayList', res.data.project)
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

  updateDownPay: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/down-payment/${pk}/`, formData)
      .then(res => {
        dispatch('fetchDownPayList', res.data.project)
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

  deleteDownPay: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/down-payment/${pk}/`)
      .then(() => {
        dispatch('fetchDownPayList', project)
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

  fetchPaymentList: ({ commit }: any, payload: any) => {
    const { project } = payload
    let url = `/payment-list/?project=${project}`
    if (payload.from_date) url += `&from_deal_date=${payload.from_date}`
    if (payload.to_date) url += `&to_deal_date=${payload.to_date}`
    if (payload.pay_order) url += `&installment_order=${payload.pay_order}`
    if (payload.pay_account) url += `&bank_account=${payload.pay_account}`
    if (payload.no_contract) url += `&no_contract=${payload.no_contract}`
    if (payload.search) url += `&search=${payload.search}`
    const page = payload.page ? payload.page : 1
    if (payload.page) url += `&page=${page}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_PAYMENT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchPaySumList: ({ commit }: any, project: any) => {
    api
      .get(`/payment-sum/?project=${project}`)
      .then(res => {
        commit(FETCH_PAYMENT_SUM_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchContNumList: ({ commit }: any, project: any) => {
    api
      .get(`/contract-num/?project=${project}`)
      .then(res => {
        commit(FETCH_CONTRACT_NUM_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },
}

export default actions
