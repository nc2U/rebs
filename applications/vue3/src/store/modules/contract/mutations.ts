import {
  FETCH_CONT_SUMMARY_LIST,
  FETCH_CONTRACT,
  FETCH_CONTRACT_LIST,
  FETCH_ORDER_GROUP_LIST,
  FETCH_SUBS_SUMMARY_LIST,
  FETCH_KEY_UNIT_LIST,
  FETCH_HOUSE_UNIT_LIST,
  FETCH_CONT_RELEASE_LIST,
} from '@/store/modules/contract/mutations-types'
import { ContractState, Contract } from '@/store/modules/contract/state'

const mutations = {
  [FETCH_CONTRACT_LIST]: (state: ContractState, payload: any) => {
    state.contractList = payload.results
    state.contractsCount = payload.count
  },

  [FETCH_CONTRACT]: (state: ContractState, payload: Contract) =>
    (state.contract = payload),

  [FETCH_ORDER_GROUP_LIST]: (state: ContractState, payload: any) =>
    (state.orderGroupList = payload.results),

  [FETCH_SUBS_SUMMARY_LIST]: (state: ContractState, payload: any) =>
    (state.subsSummaryList = payload.results),

  [FETCH_CONT_SUMMARY_LIST]: (state: ContractState, payload: any) =>
    (state.contSummaryList = payload.results),

  [FETCH_KEY_UNIT_LIST]: (state: ContractState, payload: any) =>
    (state.keyUnitList = payload.results),

  [FETCH_HOUSE_UNIT_LIST]: (state: ContractState, payload: any) =>
    (state.houseUnitList = payload.results),

  [FETCH_CONT_RELEASE_LIST]: (state: ContractState, payload: any) => {
    state.contReleaseList = payload.results
    state.contReleaseCount = payload.count
  },
}

export default mutations
