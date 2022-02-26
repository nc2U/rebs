import { CashesState } from '@/store/modules/comCash/state'

const getters = {
  getCashLogs: (state: CashesState) => {
    return state.cashBookList
      ? state.cashBookList.map((c: any) => ({
          pk: c.pk,
          deal_date: c.deal_date,
          sort: c.sort
            ? state.sortList
                .filter(sort => sort.pk === c.sort)
                .map(sort => sort.name)[0]
            : '',
          account_d1: c.account_d1
            ? state.comAccD1List
                .filter(d1 => d1.pk === c.account_d1)
                .map(d1 => d1.name)[0]
            : '',
          account_d3: c.account_d3
            ? state.comAccD3List
                .filter(d3 => d3.pk === c.account_d3)
                .map(d3 => d3.name)[0]
            : '',
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
