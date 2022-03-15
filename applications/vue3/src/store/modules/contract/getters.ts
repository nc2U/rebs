import { ContractState } from '@/store/modules/contract/state'

const getters = {
  contractIndex: (state: ContractState) => {
    return state.contractList.map(c => ({
      pk: c.pk,
      serial_number: c.serial_number,
      order_group: c.order_group,
      unit_type: c.unit_type.name,
      type_color: c.unit_type.color,
      house_unit: c.keyunit?.houseunit?.__str__ || '',
      contractor: c.contractor?.name,
      last_paid_order:
        c.payments.length !== 0
          ? c.payments
              .sort((a, b) =>
                a.installment_order.pay_time < b.installment_order.pay_time
                  ? 1
                  : -1,
              )
              .map(p => p.installment_order.__str__)[0]
          : '-',
      total_paid:
        c.payments.length !== 0
          ? c.payments.map(o => o.income).reduce((res, item) => res + item)
          : 0,
      is_registed: c.contractor?.is_registed,
      address: c.contractor?.contractoraddress?.dm_address1,
      cell_phone: c.contractor?.contractorcontact?.cell_phone,
      contract_date: c.contractor?.contract_date,
    }))
  },

  contractPages: (state: ContractState) => (itemsPerPage: number) => {
    return Math.ceil(state.contractsCount / itemsPerPage)
  },
}

export default getters
