import { CashesState } from '@/store/modules/comCash/state'

const getters = {
  getCashLogs: (state: CashesState) => {
    return state.cashBookList
      ? state.cashBookList.map((c: any) => ({
          pk: c.pk,
          deal_date: c.deal_date,
          sort: c.sort_desc,
          main_account: c.main_account_desc,
          account: c.account, //state.comAccD1List
          // ? state.comAccD1List
          //     .filter((d: any) => d.pk === c.project_account_d1)
          //     .map((d: any) => d.name)[0]
          // : [],
          content: c.content,
          trader: c.trader,
          bank_account: state.comBankList
            ? state.comBankList
                .filter((b: any) => b.pk === c.bank_account)
                .map((b: any) => b.alias_name)[0]
            : [],
          income: c.income ? c.income : 0,
          outlay: c.outlay ? c.outlay : 0,
          evidence: c.evidence_desc,
        }))
      : []
  },

  cashesPages: (state: CashesState) => (itemsPerPage: number) =>
    Math.ceil(state.cashBookCount / itemsPerPage),
}

export default getters
