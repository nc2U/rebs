import {
  FETCH_CONTRACT,
  FETCH_CONTRACT_LIST,
  FETCH_ORDER_GROUP_LIST,
} from '@/store/modules/contract/mutations-types'
import { ContractState, Contract } from '@/store/modules/contract/state'

const mutations = {
  [FETCH_CONTRACT_LIST]: (state: ContractState, payload: any) => {
    state.contractList = payload.results
  },

  [FETCH_CONTRACT]: (state: ContractState, payload: Contract) => {
    state.contract = payload
  },

  [FETCH_ORDER_GROUP_LIST]: (state: ContractState, payload: any) => {
    state.orderGroupList = payload.results
  },
}

export default mutations
