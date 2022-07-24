import {
  FETCH_PRICE_LIST,
  FETCH_PAY_ORDER_LIST,
  FETCH_PAY_ORDER,
  FETCH_DWON_PAYMENT,
  FETCH_PAYMENT_LIST,
  FETCH_ALL_PAYMENT_LIST,
  FETCH_PAYMENT_SUM_LIST,
  FETCH_CONTRACT_NUM_LIST,
} from '@/store/modules/payment/mutations-types'
import { PaymentState } from '@/store/modules/payment/state'

const mutations = {
  updateState: (state: PaymentState, payload: any) => {
    Object.keys(payload).forEach(key => {
      state[key] = payload[key]
    })
  },

  [FETCH_PRICE_LIST]: (state: PaymentState, payload: any) =>
    (state.priceList = payload.results),

  [FETCH_PAY_ORDER_LIST]: (state: PaymentState, payload: any) =>
    (state.payOrderList = payload.results),

  [FETCH_PAY_ORDER]: (state: PaymentState, payload: any) =>
    (state.payOrder = payload),

  [FETCH_DWON_PAYMENT]: (state: PaymentState, payload: any) =>
    (state.downPayList = payload.results),

  [FETCH_PAYMENT_LIST]: (state: PaymentState, payload: any) => {
    state.paymentList = payload.results
    state.paymentsCount = payload.count
  },

  [FETCH_ALL_PAYMENT_LIST]: (state: PaymentState, payload: any) => {
    state.AllPaymentList = payload.results
  },

  [FETCH_PAYMENT_SUM_LIST]: (state: PaymentState, paload: any) =>
    (state.paySumList = paload.results),

  [FETCH_CONTRACT_NUM_LIST]: (state: PaymentState, payload: any) =>
    (state.contNumList = payload.results),
}

export default mutations
