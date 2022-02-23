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
  __str__: string
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

interface ProjectBankAccount {
  pk: number
  project: number
  bankcode: number
  alias_name: string
  number: string
  holder: string
  open_date: string | null
  note: string
  inactive: boolean
  directpay: boolean
}

interface ProjectCashBook {
  pk: number
  project: number
  cash_category1: string
  project_account_d1: number | null
  project_account_d2: number | null
  is_record_separate: boolean
  is_contract_payment: boolean
  contract: number | null
  installment_order: number | null
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
}

export interface PaymentState {
  priceList: Price[]
  payOrderList: PayOrder[]
  downPayList: DownPay[]
  pBankAccountList: ProjectBankAccount[]
  pCashBookList: ProjectCashBook[]
  paymentList: ProjectCashBook[]
  paymentsCount: number
}

const state: PaymentState = {
  priceList: [],
  payOrderList: [],
  downPayList: [],
  pBankAccountList: [],
  pCashBookList: [],
  paymentList: [],
  paymentsCount: 0,
}

export default state
