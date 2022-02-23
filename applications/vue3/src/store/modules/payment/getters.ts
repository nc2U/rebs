import { PaymentState } from '@/store/modules/payment/state'

const getters = {
  getPayments: (state: PaymentState) => {
    return state.paymentList
      ? state.paymentList.map((p: any) => ({
          pk: p.pk,
          deal_date: p.deal_date,
          contract: p.contract,
          order_group: p.contract ? p.contract.order_group : '-',
          type_color: p.contract ? p.contract.unit_type.color : '-',
          type_name: p.contract ? p.contract.unit_type.name : '-',
          serial_number: p.contract ? p.contract.serial_number : '-',
          contractor: p.contract ? p.contract.contractor : '-',
          income: p.income,
          installment_order: p.installment_order,
          bank_account: p.bank_account,
          trader: p.trader,
        }))
      : []
  },
  paymentPages: (state: PaymentState) => (itemsPerPage: number) => {
    return Math.ceil(state.paymentsCount / itemsPerPage)
  },
}

export default getters
