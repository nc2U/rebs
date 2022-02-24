import { ProjectCashState } from '@/store/modules/proCash/state'

const getters = {
  getProCashes: (state: ProjectCashState) => {
    return state.proCashBookList
      ? state.proCashBookList.map((p: any) => ({
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

  proCashPages: (state: ProjectCashState) => (itemsPerPage: number) =>
    Math.ceil(state.proCashesCount / itemsPerPage),
}

export default getters
