import { State } from '@/store'
import { SalesBillIssue } from '@/store/types/notice'

export interface NoticeState extends State {
  billIssue: SalesBillIssue | null
}

const state: NoticeState = {
  billIssue: null,
}

export default state
