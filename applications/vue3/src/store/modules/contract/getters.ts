import { ContractState } from '@/store/modules/contract/state'

const getters = {
  OrderGroupByProject: (state: ContractState) => (pk: any) => {
    return state.orderGroupList.filter((og) => og?.project === pk)
  },
}

export default getters
