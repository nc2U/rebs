export interface ProjectAccountD1 {
  pk: number
  sort: string
  sort_desc: string
  code: string
  name: string
  description: string
}

export interface ProjectAccountD2 {
  pk: number
  d1: number
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
  sort: string
  sort_desc: string
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
  evidence_desc: string
  note: string
  deal_date: string
}

export interface ProjectCashState {
  accountD1List: ProjectAccountD1[]
  accountD2List: ProjectAccountD2[]
  proBankAccountList: ProjectBankAccount[]
  proCashBookList: ProjectCashBook[]
  proCashesCount: number
}

const state = {
  accountD1List: [],
  accountD2List: [],
  pBankAccountList: [],
  proCashBookList: [],
  proCashesCount: 0,
}

export default state
