interface CompanyBank {
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

interface CashBook {
  pk: number
  company: number
  cash_category1: string
  cash_category1_desc: string
  cash_category2: string
  cash_category2_desc: string
  account: number | null
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
  comBankList: CompanyBank[]
  cashBookList: CashBook[]
  cashBookCount: number
}

const state = {
  comBankList: [],
  cashBookList: [],
  cashBookCount: 0,
}

export default state
