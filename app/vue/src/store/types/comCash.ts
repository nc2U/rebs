export interface AccountSort {
  pk: number
  name: string
  accounts: number[]
}

export interface AccountD1 {
  pk: number
  code: string
  name: string
  description: string
}

export interface AccountD2 {
  pk: number
  d1: number
  code: string
  name: string
  description: string
}

export interface AccountD3 {
  pk: number
  d2: number
  code: string
  name: string
  is_special: boolean
  description: string
}

export interface CompanyBank {
  pk: number
  company: number
  division: number | null
  bankcode: number
  alias_name: string
  number: string
  holder: string
  open_date: string | null
  note: string
  inactive: boolean
}

export interface BalanceByAccount {
  bank_acc: string
  date_inc: number
  date_out: number
  inc_sum: number | null
  out_sum: number | null
}

export interface CashBook {
  pk: number | null
  company: number | null
  sort: number | null
  sort_desc?: string
  account_d1: number | null
  account_d1_desc?: string
  account_d2: number | null
  account_d3: number | null
  account_d3_desc?: string
  content: string
  trader: string
  bank_account: number | null
  bank_account_desc?: string
  income?: number | null
  outlay?: number | null
  evidence: string
  evidence_desc?: string
  note: string
  deal_date: string
}
