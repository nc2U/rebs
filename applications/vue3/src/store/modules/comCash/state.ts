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

export interface CashBook {
  pk: number
  company: number
  sort: string
  sort_desc: string
  account_d1: string
  account_d3: number | null
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

  formAccD1List: AccountD1[]
  formAccD2List: AccountD2[]
  formAccD3List: AccountD3[]

  listAccD1List: AccountD1[]
  listAccD2List: AccountD2[]
  listAccD3List: AccountD3[]

  comBankList: CompanyBank[]
  cashBookList: CashBook[]
  cashBookCount: number
}

const state = {
  sortList: [],

  formAccD1List: [],
  formAccD2List: [],
  formAccD3List: [],

  listAccD1List: [],
  listAccD2List: [],
  listAccD3List: [],

  comBankList: [],
  cashBookList: [],
  cashBookCount: 0,
}

export default state
