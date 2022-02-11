import {
  FETCH_PRICE_LIST,
  FETCH_PAY_ORDER_LIST,
  FETCH_DWON_PAYMENT,
} from '@/store/modules/cash/mutations-types'
import { CashState } from '@/store/modules/cash/state'

const mutations = {
  [FETCH_PRICE_LIST]: (state: CashState, payload: any) => {
    state.priceList = payload.results
  },

  [FETCH_PAY_ORDER_LIST]: (state: CashState, payload: any) => {
    state.payOrderList = payload.results
  },

  [FETCH_DWON_PAYMENT]: (state: CashState, payload: any) => {
    state.downPayList = payload.results
  },
}

export default mutations
