import {
  FETCH_P_ACC_SORT_LIST,
  FETCH_ALL_ACC_D1_LIST,
  FETCH_ALL_ACC_D2_LIST,
  FETCH_FORM_ACC_D1_LIST,
  FETCH_FORM_ACC_D2_LIST,
  FETCH_P_BANK_ACCOUNT_LIST,
  FETCH_P_DATE_CASHBOOK,
  FETCH_P_CASHBOOK_LIST,
  FETCH_P_IMPREST_LIST,
  FETCH_BALANCE_BY_ACC_LIST,
  FETCH_P_BUDGET_LIST,
  FETCH_EXEC_AMOUNT_LIST,
} from '@/store/modules/proCash/mutations-types'
import { ProjectCashState } from '@/store/modules/proCash/state'

const mutations = {
  [FETCH_P_ACC_SORT_LIST]: (state: ProjectCashState, payload: any) =>
    (state.sortList = payload.results),

  [FETCH_ALL_ACC_D1_LIST]: (state: ProjectCashState, payload: any) =>
    (state.allAccD1List = payload.results),

  [FETCH_ALL_ACC_D2_LIST]: (state: ProjectCashState, payload: any) =>
    (state.allAccD2List = payload.results),

  [FETCH_FORM_ACC_D1_LIST]: (state: ProjectCashState, payload: any) =>
    (state.formAccD1List = payload.results),

  [FETCH_FORM_ACC_D2_LIST]: (state: ProjectCashState, payload: any) =>
    (state.formAccD2List = payload.results),

  [FETCH_P_BANK_ACCOUNT_LIST]: (state: ProjectCashState, payload: any) =>
    (state.proBankAccountList = payload.results),

  [FETCH_BALANCE_BY_ACC_LIST]: (state: ProjectCashState, payload: any) =>
    (state.balanceByAccList = payload.results),

  [FETCH_P_DATE_CASHBOOK]: (state: ProjectCashState, payload: any) =>
    (state.proDateCashBook = payload.results),

  [FETCH_P_BUDGET_LIST]: (state: ProjectCashState, payload: any) =>
    (state.proBudgetList = payload.results),

  [FETCH_EXEC_AMOUNT_LIST]: (state: ProjectCashState, payload: any) =>
    (state.execAmountList = payload.results),

  [FETCH_P_CASHBOOK_LIST]: (state: ProjectCashState, payload: any) => {
    state.proCashBookList = payload.results
    state.proCashesCount = payload.count
  },

  [FETCH_P_IMPREST_LIST]: (state: ProjectCashState, payload: any) => {
    state.proImprestList = payload.results
    state.proImprestCount = payload.count
  },
}

export default mutations
