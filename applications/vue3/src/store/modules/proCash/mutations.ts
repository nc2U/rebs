import {
  FETCH_P_BANK_ACCOUNT_LIST,
  FETCH_P_CASHBOOK_LIST,
} from '@/store/modules/proCash/mutations-types'
import { ProjectCashState } from '@/store/modules/proCash/state'

const mutations = {
  [FETCH_P_BANK_ACCOUNT_LIST]: (state: ProjectCashState, payload: any) =>
    (state.pBankAccountList = payload.results),

  [FETCH_P_CASHBOOK_LIST]: (state: ProjectCashState, payload: any) => {
    state.pCashBookList = payload.results
    state.proCashesCount = payload.count
  },
}

export default mutations
