import {
  FETCH_PRICE_LIST,
  FETCH_PAY_ORDER_LIST,
  FETCH_DWON_PAYMENT,
  FETCH_PAYMENT_LIST,
  FETCH_PAYMENT_SUM_LIST,
  FETCH_CONTRACT_NUM_LIST,
  FETCH_PAYMENT,
} from '@/store/modules/payment/mutations-types'
import { PaymentState } from '@/store/modules/payment/state'
import { ProjectCashBook } from '@/store/modules/proCash/state'

const mutations = {
  [FETCH_PRICE_LIST]: (state: PaymentState, payload: any) =>
    (state.priceList = payload.results),

  [FETCH_PAY_ORDER_LIST]: (state: PaymentState, payload: any) =>
    (state.payOrderList = payload.results),

  [FETCH_DWON_PAYMENT]: (state: PaymentState, payload: any) =>
    (state.downPayList = payload.results),

  [FETCH_PAYMENT_LIST]: (state: PaymentState, payload: any) => {
    state.paymentList = payload.results
    state.paymentsCount = payload.count
  },

  [FETCH_PAYMENT]: (state: PaymentState, payload: ProjectCashBook) =>
    (state.payment = payload),

  [FETCH_PAYMENT_SUM_LIST]: (state: PaymentState, paload: any) =>
    (state.paySumList = paload.results),

  [FETCH_CONTRACT_NUM_LIST]: (state: PaymentState, payload: any) =>
    (state.contNumList = payload.results),
}

export default mutations
