import { NoticeState, SalesBillIssue } from '@/store/modules/notice/state'
import { FETCH_SALES_BILL_ISSUE } from '@/store/modules/notice/mutations-types'

const mutations = {
  [FETCH_SALES_BILL_ISSUE]: (state: NoticeState, payload: SalesBillIssue) =>
    (state.billIssue = payload),
}

export default mutations
