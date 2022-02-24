export interface ProjectAccountD1 {
  sort: string
  sort_desc: string
  name: string
  description: string
}

export interface ProjectAccountD2 {
  d1: ProjectAccountD1
  code: string
  sub_title: string
  name: string
  description: string
}

export interface ProjectBankAccount {
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

export interface ProjectCashBook {
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

export interface ProjectCashState {
  d1List: ProjectAccountD1[]
  d2List: ProjectAccountD2[]
  pBankAccountList: ProjectBankAccount[]
  pCashBookList: ProjectCashBook[]
  proCashesCount: number
}

const state = {
  d1List: [],
  d2List: [],
  pBankAccountList: [],
  pCashBookList: [],
  proCashesCount: 0,
}

export default state
