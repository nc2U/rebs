import { CashesState } from '@/store/modules/comCash/state'

const getters = {
  getCashLogs: (state: CashesState) => {
    return state.cashBookList
      ? state.cashBookList.map((c: any) => ({
          pk: c.pk,
          company: c.company,
          deal_date: c.deal_date,
          sort: c.sort,
          sort_desc: c.sort
            ? state.sortList
                .filter(sort => sort.pk === c.sort)
                .map(sort => sort.name)[0]
            : '',
          account_d1: c.account_d1,
          account_d1_desc: c.account_d1
            ? state.comAccD1List
                .filter(d1 => d1.pk === c.account_d1)
                .map(d1 => d1.name)[0]
            : '',
          account_d2: c.account_d2,
          account_d3: c.account_d3,
          account_d3_desc: c.account_d3
            ? state.comAccD3List
                .filter(d3 => d3.pk === c.account_d3)
                .map(d3 => d3.name)[0]
            : '',
          content: c.content,
          trader: c.trader,
          bank_account: c.bank_account,
          bank_account_desc: state.comBankList
            ? state.comBankList
                .filter((b: any) => b.pk === c.bank_account)
                .map((b: any) => b.alias_name)[0]
            : [],
          income: c.income,
          outlay: c.outlay,
          evidence: c.evidence,
          evidence_desc: c.evidence_desc,
          note: c.note,
        }))
      : []
  },

  cashesPages: (state: CashesState) => (itemsPerPage: number) =>
    Math.ceil(state.cashBookCount / itemsPerPage),
}

export default getters
