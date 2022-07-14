interface ContractorContact {
  pk: number
  cell_phone: string
  email: string
}

interface ContractorAddress {
  pk: number
  dm_address1: string
}

interface ContractorInContract {
  pk: number
  name: string
  is_registed: boolean
  contractoraddress: ContractorAddress | null
  contractorcontact: ContractorContact | null
  status: string
  contract_date: string | null
}

export interface OrderGroup {
  pk: number
  project: number
  order_number: number
  sort: string
  sort_desc: string
  order_group_name: string
}

interface UnitType {
  pk: number
  name: string
  color: string
  average_price: number
}

interface HouseUnit {
  pk: number
  __str__: string
}

interface KeyUnit {
  pk: number
  houseunit: HouseUnit | null
}

interface InstallmentOrder {
  pk: number
  pay_time: number
  pay_name: string
  __str__: string
}

interface SalesPrice {
  pk: number
  project: number
  order_group: number
  unit_type: number
  unit_floor_type: number
  price_build: number | null
  price_land: number | null
  price_tax: number | null
  price: number
}

interface DownPayment {
  pk: number
  project: number
  order_group: number
  unit_type: number
  number_payments: number
  payment_amount: number
}

interface Payment {
  pk: number
  deal_date: string
  income: number
  bank_account: number
  trader: string
  installment_order: InstallmentOrder
}

export interface Contract {
  pk: number
  project: number
  serial_number: string
  activation: boolean
  order_group: number
  unit_type: UnitType
  keyunit: KeyUnit | null
  payments: Payment[]
  contractor: ContractorInContract | null
  user: number
}

export interface Contractor {
  pk: number
  contract: number
  name: string
  birth_date: string
  gender: string
  is_registed: boolean
  status: string
  reservation_date: string | null
  contract_date: string | null
  note: string
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

interface ContractRelease {
  pk: number
  project: number
  contractor: number
  status: string
  refund_amount: number
  refund_account_bank: string
  refund_account_number: string
  refund_account_depositor: string
  request_date: string
  completion_date: string
  note: string
}

export interface ContractState {
  contractList: Contract[]
  contractsCount: number
  contract: Contract | null
  contractorList: Contractor[]
  contractor: Contractor | null
  subsSummaryList: SubsSummary[]
  contSummaryList: ContractSummary[]
  orderGroupList: OrderGroup[]
  keyUnitList: KeyUnit[]
  houseUnitList: HouseUnit[]
  salesPriceList: SalesPrice[]
  downPaymentList: DownPayment[]
  contReleaseList: ContractRelease[]
  contReleaseCount: number
  contRelease: ContractRelease | null
}

const state = {
  contractList: [],
  contractsCount: 0,
  contract: null,
  contractorList: [],
  contractor: null,
  subsSummaryList: [],
  contSummaryList: [],
  orderGroupList: [],
  keyUnitList: [],
  houseUnitList: [],
  salesPriceList: [],
  downPaymentList: [],
  contReleaseList: [],
  contReleaseCount: 0,
  contRelease: null,
}

export default state
