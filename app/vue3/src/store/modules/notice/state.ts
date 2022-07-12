export declare interface SalesBillIssue {
  pk: number
  project: number
  now_payment_order: number
  host_name: string
  host_tel: string
  agency: string
  agency_tel: string
  bank_account1: string
  bank_number1: string
  bank_host1: string
  bank_account2: string
  bank_number2: string
  bank_host2: string
  zipcode: string
  address1: string
  address2: string
  address3: string
  title: string
  content: string
}

export declare interface NoticeState {
  billIssueList: SalesBillIssue[]
  billIssue: SalesBillIssue | null
}

const state: NoticeState = {
  billIssueList: [],
  billIssue: null,
}

export default state
