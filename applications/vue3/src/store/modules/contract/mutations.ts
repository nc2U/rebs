import {
  FETCH_ORDER_GROUP,
  FETCH_ORDER_GROUP_LIST,
} from '@/store/modules/contract/mutations-types'
import { ContractState, OrderGroup } from '@/store/modules/contract/state'

const mutations = {
  [FETCH_ORDER_GROUP_LIST]: (state: ContractState, payload: any) => {
    state.orderGroupList = payload.results
  },

  [FETCH_ORDER_GROUP]: (state: ContractState, payload: OrderGroup) => {
    state.orderGroup = payload
  },
}

export default mutations
