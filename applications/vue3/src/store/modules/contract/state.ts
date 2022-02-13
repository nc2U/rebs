interface UnitNumber {
  pk: number
  project: string
  floor_type: string
  bldg_no: string
  bldg_unit_no: string
  contract_unit: number
  bldg_line: number
  floor_no: number
  is_hold: boolean
  hold_reason: string
}

interface ContractUnit {
  pk: number
  project: string
  unit_type: string
  unit_code: string
  unitnumber: UnitNumber | null
  contract: number
}

interface ContractorAddress {
  pk: number
  contractor: number
  id_zipcode: string
  id_address1: string
  id_address2: string
  id_address3: string
  dm_zipcode: string
  dm_address1: string
  dm_address2: string
  dm_address3: string
}

interface ContractorContact {
  pk: number
  contractor: number
  cell_phone: string
  home_phone: string
  other_phone: string
  email: string
}

interface Contractor {
  pk: number
  contract: number
  name: string
  birth_date: string
  gender: string
  contractoraddress: ContractorAddress | null
  contractorcontact: ContractorContact | null
  is_registed: boolean
  status: string
  reservation_date: string | null
  contract_date: string
  note: string
}

export interface Contract {
  pk: number
  project: number
  order_group: number
  serial_number: string
  activation: boolean
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
  contract: Contract | null
  orderGroupList: OrderGroup[]
}

const state = {
  contractList: [],
  contract: null,
  orderGroupList: [],
}

export default state
