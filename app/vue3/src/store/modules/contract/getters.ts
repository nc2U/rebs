import { ContractState } from '@/store/modules/contract/state'

const getters = {
  contractIndex: (state: ContractState) => {
    return state.contractList.map(c => ({
      pk: c.pk,
      serial_number: c.serial_number,
      order_group: c.order_group,
      unit_type: c.unit_type.name,
      type_color: c.unit_type.color,
      house_unit: c.keyunit?.houseunit?.__str__ || '[미정]',
      contractor: c.contractor?.name,
      total_paid:
        c.payments.length !== 0
          ? c.payments.map(o => o.income).reduce((res, item) => res + item)
          : 0,
      last_paid_order:
        c.payments.length !== 0
          ? c.payments
              .filter(p => p.installment_order !== null)
              .map(p => p.installment_order)
              .pop()
          : '-',
      is_registed: c.contractor?.is_registed,
      address: c.contractor?.contractoraddress?.dm_address1,
      cell_phone: c.contractor?.contractorcontact?.cell_phone,
      contract_date: c.contractor?.contract_date,
    }))
  },

  contBillIndex: (state: ContractState) => {
    return state.contractList.map(c => ({
      pk: c.pk,
      ctor_pk: c.contractor?.pk,
      serial_number: c.serial_number,
      order_group: c.order_group,
      type_pk: c.unit_type.pk,
      unit_type: c.unit_type.name,
      type_color: c.unit_type.color,
      average_price: c.unit_type.average_price,
      house_unit: c.keyunit?.houseunit,
      contractor: c.contractor?.name,
      total_paid:
        c.payments.length !== 0
          ? c.payments.map(o => o.income).reduce((res, item) => res + item)
          : 0,
      last_paid_order:
        c.payments.length !== 0
          ? c.payments
              .filter(p => p.installment_order !== null)
              .map(p => p.installment_order)
              .pop()
          : '-',
      contract_date: c.contractor?.contract_date,
    }))
  },

  contractPages: (state: ContractState) => (itemsPerPage: number) => {
    return Math.ceil(state.contractsCount / itemsPerPage)
  },

  releasePages: (state: ContractState) => (itemsPerPage: number) => {
    return Math.ceil(state.contReleaseCount / itemsPerPage)
  },
}

export default getters
