import { ContractState } from '@/store/modules/contract/state'

const getters = {
  contractPages: (state: ContractState) => (itemsPerPage: number) => {
    return Math.ceil(state.contractsCount / itemsPerPage)
  },

  releasePages: (state: ContractState) => (itemsPerPage: number) => {
    return Math.ceil(state.contReleaseCount / itemsPerPage)
  },
}

export default getters
