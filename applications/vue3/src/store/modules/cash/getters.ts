import { CashState } from '@/store/modules/cash/state'

const getters = {
  getPaymentList: (state: CashState) =>
    state.paymentList
      ? state.paymentList.map((p: any) => ({
          pk: p.pk,
          contract: p.contract,
          trader: p.trader,
          income: p.income,
          deal_date: p.deal_date,
          installment_order: p.installment_order,
          bank_account: p.bank_account,
        }))
      : [],
}

export default getters
