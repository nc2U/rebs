import { ContractState, ContractSummary } from '@/store/modules/contract/state'

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
      is_registed: c.contractor?.is_registed,
      address: c.contractor?.contractoraddress?.dm_address1,
      cell_phone: c.contractor?.contractorcontact?.cell_phone,
      contract_date: c.contractor?.contract_date,
    }))
  },

  contractPages: (state: ContractState) => (itemsPerPage: number) => {
    return Math.ceil(state.contractsCount / itemsPerPage)
  },

  getSubs: (state: ContractState) => (type?: number) => {
    const subs = state.contSummary.filter((c: any) => c.contractor === '1')
    return !type
      ? subs.length
      : subs.filter((c: any) => c.unit_type === type).length
  },

  getConts: (state: ContractState) => (order?: number, type?: number) => {
    let conts = state.contSummary.filter((c: any) => c.contractor === '2')
    if (order) conts = conts.filter((c: any) => c.order_group === order)
    if (type) conts = conts.filter((c: any) => c.unit_type === type)
    return conts.length
  },
}

export default getters
