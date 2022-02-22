import { CashState } from '@/store/modules/cash/state'

const getters = {
  paymentPages: (state: CashState) => (itemsPerPage: number) => {
    return Math.ceil(state.paymentsCount / itemsPerPage)
  },
}

export default getters
