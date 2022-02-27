import { ProjectCashState } from '@/store/modules/proCash/state'

const getters = {
  getProCashes: (state: ProjectCashState) => {
    return state.proCashBookList
      ? state.proCashBookList.map((p: any) => ({
          pk: p.pk,
          project: p.project,
          sort: state.sortList
            ? state.sortList.filter(s => s.pk === p.sort).map(s => s.name)[0]
            : '',
          project_account_d1: state.formAccD1List
            ? state.formAccD1List
                .filter(d => d.pk === p.project_account_d1)
                .map(d => d.name)[0]
            : '',
          project_account_d2: state.formAccD2List
            ? state.formAccD2List
                .filter(d => d.pk === p.project_account_d2)
                .map(d => d.name)[0]
            : '',
          is_contract_payment: p.is_contract_payment,
          content: p.content,
          trader: p.trader,
          bank_account: state.proBankAccountList
            ? state.proBankAccountList
                .filter(b => b.pk === p.bank_account)
                .map(b => b.alias_name)[0]
            : '',
          income: p.income,
          outlay: p.outlay,
          evidence: p.evidence_desc,
          deal_date: p.deal_date,
        }))
      : []
  },

  proCashPages: (state: ProjectCashState) => (itemsPerPage: number) =>
    Math.ceil(state.proCashesCount / itemsPerPage),
}

export default getters
