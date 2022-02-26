import {
  FETCH_P_ACC_SORT_LIST,
  FETCH_ACCOUNT_D1_LIST,
  FETCH_ACCOUNT_D2_LIST,
  FETCH_P_BANK_ACCOUNT_LIST,
  FETCH_P_CASHBOOK_LIST,
} from '@/store/modules/proCash/mutations-types'
import { ProjectCashState } from '@/store/modules/proCash/state'

const mutations = {
  [FETCH_P_ACC_SORT_LIST]: (state: ProjectCashState, payload: any) =>
    (state.sortList = payload.results),

  [FETCH_ACCOUNT_D1_LIST]: (state: ProjectCashState, payload: any) =>
    (state.accountD1List = payload.results),

  [FETCH_ACCOUNT_D2_LIST]: (state: ProjectCashState, payload: any) =>
    (state.accountD2List = payload.results),

  [FETCH_P_BANK_ACCOUNT_LIST]: (state: ProjectCashState, payload: any) =>
    (state.proBankAccountList = payload.results),

  [FETCH_P_CASHBOOK_LIST]: (state: ProjectCashState, payload: any) => {
    state.proCashBookList = payload.results
    state.proCashesCount = payload.count
  },
}

export default mutations
