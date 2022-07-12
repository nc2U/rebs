import { NoticeState, SalesBillIssue } from '@/store/modules/notice/state'
import {
  FETCH_SALES_BILL_ISSUE_LIST,
  FETCH_SALES_BILL_ISSUE,
} from '@/store/modules/notice/mutations-types'

const mutations = {
  [FETCH_SALES_BILL_ISSUE_LIST]: (state: NoticeState, payload: any) =>
    (state.billIssueList = payload.results),

  [FETCH_SALES_BILL_ISSUE]: (state: NoticeState, payload: SalesBillIssue) =>
    (state.billIssue = payload),
}

export default mutations
