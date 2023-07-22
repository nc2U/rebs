export interface SimpleCont {
  pk: number
  project: number
  order_group: number
  unit_type: number
  serial_number: string
  activation: boolean
}

export interface Contract {
  pk: number
  project: number
  order_group: number
  unit_type: number
  serial_number: string
  activation: boolean
  keyunit: KeyUnit | null
  contractprice: ContPrice | null
  contractor: ContractorInContract | null
  payments: Payment[]
  total_paid: number
  last_paid_order: InstallmentOrder | null
  order_group_desc: {
    pk: number
    sort: string
    order_group_name: string
  }
  unit_type_desc: UnitType
}

export interface KeyUnit {
  pk: number
  unit_code: string
  houseunit: HouseUnit | null
}

export interface HouseUnit {
  pk: number
  __str__: string
  floor_type: number
}

export interface ContPrice {
  pk: number
  price: number
  price_build: number | null
  price_land: number | null
  price_tax: number | null
  down_pay: number
  middle_pay: number
  remain_pay: number
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

interface ContractorAddress {
  pk: number
  dm_address1: string
}

interface ContractorContact {
  pk: number
  cell_phone: string
  email: string
}

export interface Payment {
  pk: number
  deal_date: string
  income: number
  bank_account: number
  trader: string
  installment_order: InstallmentOrder
}

interface InstallmentOrder {
  pk: number
  pay_sort: string
  pay_time: number
  pay_name: string
  __str__: string
}

export interface UnitType {
  pk: number
  name: string
  color: string
  average_price: number
}

export interface OrderGroup {
  pk: number
  project: number
  order_number: number
  sort: '1' | '2'
  sort_desc: string
  order_group_name: string
}

export interface SalesPrice {
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

export interface DownPayment {
  pk: number
  project: number
  order_group: number
  unit_type: number
  number_payments: number
  payment_amount: number
}

export interface Contractor {
  pk: number
  contract: number
  name: string
  __str__: string
  birth_date: string | null
  gender: string
  is_registed: boolean
  status: string
  reservation_date: string | null
  contract_date: string | null
  note: string
  successions: SimpleSuccession[]
  contractorrelease: number | null
}

interface SimpleSuccession {
  pk: number
  is_approval: boolean
}

export interface SubsSummary {
  order_group: number
  unit_type: number
  conts_num: number
  price_sum: number
}

export type ContSummary = SubsSummary

export interface Succession {
  pk?: number
  contract: number | null
  seller: number | null
  buyer: number | null
  apply_date: string
  trading_date: string
  is_approval: boolean
  approval_date: string | null
  note: string
}

export interface Buyer {
  id?: number
  name: string
  birth_date: string
  gender: 'M' | 'F'
  id_zipcode: string
  id_address1: string
  id_address2: string
  id_address3: string
  dm_zipcode: string
  dm_address1: string
  dm_address2: string
  dm_address3: string
  cell_phone: string
  home_phone: string
  other_phone: string
  email: string
}

export interface ContractRelease {
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
