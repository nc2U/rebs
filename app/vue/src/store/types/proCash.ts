export interface ProjectAccountD1 {
  pk: number
  acc: string
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
  bank_num: string
  date_inc: number
  date_out: number
  inc_sum: number | null
  out_sum: number | null
}

export interface ProSepItems {
  pk?: number | null
  project_account_d1: number | null
  project_account_d2: number | null
  separated?: number | null
  is_imprest?: boolean
  content: string
  trader: string
  income?: number | null
  outlay?: number | null
  evidence?: '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | ''
  note: string
}

export interface ProjectCashBook extends ProSepItems {
  project: number | null
  sort: number | null
  is_separate?: boolean
  sepItems?: []
  contract?: number | null
  installment_order?: number | null
  refund_contractor?: number | null
  bank_account: number | null
  evidence_desc?: string
  deal_date: string
}

export type CashBookFilter = {
  project?: number
  page?: number
  from_date?: string
  to_date?: string
  order_group?: string
  unit_type?: string
  sort?: number | null
  pro_acc_d1?: number | null
  pro_acc_d2?: number | null
  bank_account?: number | null
  pay_order?: string
  pay_account?: string
  contract?: number
  no_contract?: boolean
  no_install?: boolean
  ordering?: string
  search?: string
}
