interface ContractorContact {
  pk: number
  cell_phone: string
  email: string
}

interface ContractorAddress {
  pk: number
  dm_address1: string
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

interface HouseUnit {
  pk: number
  __str__: string
}

interface KeyUnit {
  pk: number
  houseunit: HouseUnit | null
}

interface UnitType {
  name: string
  color: string
}

export interface Contract {
  pk: number
  project: number
  serial_number: string
  activation: boolean
  order_group: number
  unit_type: UnitType
  keyunit: KeyUnit | null
  contractor: Contractor | null
  user: number
}

export interface OrderGroup {
  pk: number
  project: number
  order_number: number
  sort: string
  sort_desc: string
  order_group_name: string
}

interface SubsSummary {
  order_group: number
  num_cont: number
}

export interface ContractSummary {
  project: number
  order_group: number
  unit_type: number
  contractor: string
}

export interface ContractState {
  contractList: Contract[]
  contractsCount: number
  contract: Contract | null
  subsSummaryList: SubsSummary[]
  contSummaryList: ContractSummary[]
  orderGroupList: OrderGroup[]
  keyUnitList: KeyUnit[]
}

const state = {
  contractList: [],
  contractsCount: 0,
  contract: null,
  subsSummaryList: [],
  contSummaryList: [],
  orderGroupList: [],
  keyUnitList: [],
}

export default state
