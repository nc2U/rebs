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
  is_imprest: boolean
}

export interface BalanceByAccount {
  bank_acc: string
  date_inc: number
  date_out: number
  inc_sum: number | null
  out_sum: number | null
}

export interface ProjectBudget {
  pk: number
  project: number
  account_d1: number
  account_d2: number
  budget: number
}

export interface ExecAmountToBudget {
  acc_d2: number
  all_sum: number
  month_sum: number
}

export interface ProjectCashBook {
  pk: number
  project: number
  sort: string
  sort_desc: string
  project_account_d1: number | null
  project_account_d2: number | null
  is_separate: boolean
  separated: number
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
