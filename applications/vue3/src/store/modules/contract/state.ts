interface UnitNumber {
  pk: number
  unit_type: string
  floor_type: string
  __str__: string
}

interface ContractUnit {
  pk: number
  unit_type: string
  unitnumber: UnitNumber | null
}

interface ContractorAddress {
  pk: number
  dm_address1: string
}

interface ContractorContact {
  pk: number
  cell_phone: string
  email: string
}

interface Contractor {
  pk: number
  name: string
  is_registed: boolean
  contractoraddress: ContractorAddress | null
  contractorcontact: ContractorContact | null
  status: string
  contract_date: string
}

export interface Contract {
  pk: number
  project: number
  serial_number: string
  activation: boolean
  order_group: number
  unit_type: string
  contractunit: ContractUnit | null
  contractor: Contractor | null
  user: number
}

export interface OrderGroup {
  pk: number
  url: string
  project: number
  order_number: number
  sort: string
  sort_desc: string
  order_group_name: string
}

export interface ContractState {
  contractList: Contract[]
  contractsCount: number
  contract: Contract | null
  orderGroupList: OrderGroup[]
}

const state = {
  contractList: [],
  contractsCount: 0,
  contract: null,
  orderGroupList: [],
}

export default state
