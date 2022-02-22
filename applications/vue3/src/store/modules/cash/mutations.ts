import {
  FETCH_PRICE_LIST,
  FETCH_PAY_ORDER_LIST,
  FETCH_DWON_PAYMENT,
  FETCH_P_BANK_ACCOUNT_LIST,
  FETCH_P_CASHBOOK_LIST,
  FETCH_PAYMENT_LIST,
} from '@/store/modules/cash/mutations-types'
import { CashState } from '@/store/modules/cash/state'

const mutations = {
  [FETCH_PRICE_LIST]: (state: CashState, payload: any) =>
    (state.priceList = payload.results),

  [FETCH_PAY_ORDER_LIST]: (state: CashState, payload: any) =>
    (state.payOrderList = payload.results),

  [FETCH_DWON_PAYMENT]: (state: CashState, payload: any) =>
    (state.downPayList = payload.results),

  [FETCH_P_BANK_ACCOUNT_LIST]: (state: CashState, payload: any) =>
    (state.pBankAccountList = payload.results),

  [FETCH_P_CASHBOOK_LIST]: (state: CashState, payload: any) =>
    (state.pCashBookList = payload.results),

  [FETCH_PAYMENT_LIST]: (state: CashState, payload: any) => {
    state.paymentList = payload.results
    state.paymentsCount = payload.count
  },
}

export default mutations
