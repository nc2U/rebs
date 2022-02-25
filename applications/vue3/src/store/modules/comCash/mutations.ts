import {
  FETCH_CASHBOOK_LIST,
  FETCH_COMPAY_BANK_LIST,
} from '@/store/modules/comCash/mutations-types'
import { CashesState } from '@/store/modules/comCash/state'

const mutations = {
  [FETCH_COMPAY_BANK_LIST]: (state: CashesState, payload: any) =>
    (state.comBankList = payload.results),

  [FETCH_CASHBOOK_LIST]: (state: CashesState, payload: any) => {
    state.cashBookList = payload.results
    state.cashBookCount = payload.count
  },
}

export default mutations
