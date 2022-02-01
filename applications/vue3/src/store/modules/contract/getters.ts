import { ContractState } from '@/store/modules/contract/state'

const getters = {
  OrderGroupByProject: (state: ContractState) => (id: any) => {
    return state.orderGroupList.filter((og) => og?.project === id)
  },
}

export default getters
