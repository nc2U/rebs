import {
  FETCH_ACC_SORT_LIST,
  FETCH_CASHBOOK_LIST,
  FETCH_COM_ACC_D1_LIST,
  FETCH_COM_ACC_D2_LIST,
  FETCH_COM_ACC_D3_LIST,
  FETCH_COMPAY_BANK_LIST,
} from '@/store/modules/comCash/mutations-types'
import { CashesState } from '@/store/modules/comCash/state'

const mutations = {
  [FETCH_ACC_SORT_LIST]: (state: CashesState, payload: any) =>
    (state.sortList = payload.results),

  [FETCH_COM_ACC_D1_LIST]: (state: CashesState, payload: any) =>
    (state.comAccD1List = payload.results),

  [FETCH_COM_ACC_D2_LIST]: (state: CashesState, payload: any) =>
    (state.comAccD2List = payload.results),

  [FETCH_COM_ACC_D3_LIST]: (state: CashesState, payload: any) =>
    (state.comAccD3List = payload.results),

  [FETCH_COMPAY_BANK_LIST]: (state: CashesState, payload: any) =>
    (state.comBankList = payload.results),

  [FETCH_CASHBOOK_LIST]: (state: CashesState, payload: any) => {
    state.cashBookList = payload.results
    state.cashBookCount = payload.count
  },
}

export default mutations
