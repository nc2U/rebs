import { FETCH_ORDER_GROUP_LIST } from '@/store/modules/contract/mutations-types'
import { ContractState } from '@/store/modules/contract/state'

const mutations = {
  [FETCH_ORDER_GROUP_LIST]: (state: ContractState, payload: any) => {
    state.orderGroupList = payload.results
  },
}

export default mutations
