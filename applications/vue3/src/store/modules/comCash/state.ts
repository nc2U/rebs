export interface AccountSort {
  pk: number
  name: string
  accounts: number[]
}

interface AccountD1 {
  pk: number
  code: string
  name: string
  description: string
}

interface AccountD2 {
  pk: number
  d1: number
  code: string
  name: string
  description: string
}

interface AccountD3 {
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

export interface CashBook {
  pk: number
  company: number
  sort: string
  sort_desc: string
  main_account: string
  sub_account: number | null
  content: string
  trader: string
  bank_account: number
  income: number | null
  outlay: number | null
  evidence: string
  evidence_desc: string
  note: string
  deal_date: string
  user: number
  created_at: string
  updated_at: string
}

export interface CashesState {
  sortList: AccountSort[]
  comAccD1List: AccountD1[]
  comAccD2List: AccountD2[]
  comAccD3List: AccountD3[]
  comBankList: CompanyBank[]
  cashBookList: CashBook[]
  cashBookCount: number
}

const state = {
  sortList: [],
  comAccD1List: [],
  comAccD2List: [],
  comAccD3List: [],
  comBankList: [],
  cashBookList: [],
  cashBookCount: 0,
}

export default state
