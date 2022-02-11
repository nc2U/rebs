import {
  FETCH_PRICE_LIST,
  FETCH_PRICE,
  FETCH_PAY_ORDER_LIST,
} from '@/store/modules/cash/mutations-types'
import { CashState, Price } from '@/store/modules/cash/state'

const mutations = {
  [FETCH_PRICE_LIST]: (state: CashState, payload: any) => {
    state.priceList = payload.results
  },

  [FETCH_PRICE]: (state: CashState, payload: Price) => {
    state.price = payload
  },

  [FETCH_PAY_ORDER_LIST]: (state: CashState, payload: any) => {
    state.payOrderList = payload.results
  },
}

export default mutations
