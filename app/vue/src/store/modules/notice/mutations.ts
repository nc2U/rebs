import { NoticeState } from '@/store/modules/notice/state'
import { SalesBillIssue } from '@/store/types/notice'
import { FETCH_SALES_BILL_ISSUE } from '@/store/modules/notice/mutations-types'

const mutations = {
  updateState: (state: NoticeState, payload: any) => {
    Object.keys(payload).forEach(key => {
      if (state.hasOwnProperty(key)) state[key] = payload[key]
    })
  },

  [FETCH_SALES_BILL_ISSUE]: (state: NoticeState, payload: SalesBillIssue) =>
    (state.billIssue = payload),
}

export default mutations
