import { FETCH_PRICE_LIST } from '@/store/modules/cash/mutations-types'
import { CashState } from '@/store/modules/cash/state'

const mutations = {
  [FETCH_PRICE_LIST]: (state: CashState, payload: any) => {
    state.priceList = payload.results
  },
}

export default mutations
