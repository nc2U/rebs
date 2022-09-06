export interface Contract {
  pk: number
  project: number
  order_group: {
    pk: number
    sort: string
    order_group_name: string
  }
  unit_type: UnitType
  serial_number: string
  activation: boolean
  contractor: ContractorInContract | null
  keyunit: KeyUnit | null
  payments: Payment[]
}

interface UnitType {
  pk: number
  name: string
  color: string
  average_price: number
}

export interface KeyUnit {
  pk: number
  houseunit: HouseUnit | null
}

export interface HouseUnit {
  pk: number
  __str__: string
}

interface Payment {
  pk: number
  deal_date: string
  income: number
  bank_account: number
  trader: string
  installment_order: InstallmentOrder
}

interface InstallmentOrder {
  pk: number
  pay_time: number
  pay_name: string
  __str__: string
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

interface ContractorContact {
  pk: number
  cell_phone: string
  email: string
}

interface ContractorAddress {
  pk: number
  dm_address1: string
}

export interface OrderGroup {
  pk: number
  project: number
  order_number: number
  sort: string
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
  birth_date: string
  gender: string
  is_registed: boolean
  status: string
  reservation_date: string | null
  contract_date: string | null
  note: string
}

export interface SubsSummary {
  order_group: number
  unit_type: number
  num_cont: number
}

export type ContSummary = SubsSummary

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
