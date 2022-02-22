export interface Price {
  pk: number
  project: number
  order_group: number
  unit_type: number
  unit_floor_type: number
  price_build: number
  price_land: number
  price_tax: number
  price: number
}

export interface PayOrder {
  pk: number
  project: number
  pay_sort: string
  pay_code: number
  pay_time: number
  pay_name: string
  alias_name: string
  is_pm_cost: boolean
  pay_due_date: Date
  extra_due_date: Date
}

interface DownPay {
  pk: number
  project: number
  order_group: number
  unit_type: number
  number_payments: number
  payment_amount: number
}

interface ProjectCashBook {
  pk: number
  project: number
  cash_category1: string
  project_account_d1: number
  project_account_d2: number
  is_record_separate: boolean
  is_contract_payment: boolean
  contract: number
  installment_order: number
  is_release: boolean
  is_refund_contractor: number | null
  content: string
  trader: string
  bank_account: number
  income: number | null
  outlay: number | null
  evidence: string
  note: string
  deal_date: string
  user: number
}

export interface CashState {
  priceList: Price[]
  payOrderList: PayOrder[]
  downPayList: DownPay[]
  pCashBookList: ProjectCashBook[]
  paymentList: ProjectCashBook[]
  paymentsCount: number
}

const state: CashState = {
  priceList: [],
  payOrderList: [],
  downPayList: [],
  pCashBookList: [],
  paymentList: [],
  paymentsCount: 0,
}

export default state
