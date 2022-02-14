import { ContractState } from '@/store/modules/contract/state'

const getters = {
  contractIndex: (state: ContractState) => {
    return state.contractList.map(c => ({
      pk: c.pk,
      serial_number: c.serial_number,
      order_group: c.order_group,
      unit_type: c.unit_type,
      type_color: c.contractunit?.unit_type,
      unit_number: c.contractunit?.unitnumber?.__str__ || '',
      contractor: c.contractor?.name,
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
