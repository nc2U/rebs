import { ProjectCashState } from '@/store/modules/proCash/state'

const getters = {
  getProCashes: (state: ProjectCashState) => {
    return state.proCashBookList
      ? state.proCashBookList.map((p: any) => ({
          pk: p.pk,
          deal_date: p.deal_date,
          cash_category1: p.cash_category1,
          project_account_d1: p.project_account_d1,
          project_account_d2: p.project_account_d2,
          content: p.content,
          trader: p.trader,
          bank_account: p.bank_account,
          income: p.income ? p.income : 0,
          outlay: p.outlay ? p.outlay : 0,
          evidence: p.evidence,
        }))
      : []
  },

  proCashPages: (state: ProjectCashState) => (itemsPerPage: number) =>
    Math.ceil(state.proCashesCount / itemsPerPage),
}

export default getters
