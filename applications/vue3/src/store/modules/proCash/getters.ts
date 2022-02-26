import {
  ProjectAccountD1,
  ProjectAccountD2,
  ProjectBankAccount,
  ProjectCashState,
} from '@/store/modules/proCash/state'
import { AccountSort } from '@/store/modules/comCash/state'

const getters = {
  getProCashes: (state: ProjectCashState) => {
    return state.proCashBookList
      ? state.proCashBookList.map((p: any) => ({
          pk: p.pk,
          deal_date: p.deal_date,
          sort: state.sortList
            ? state.sortList
                .filter((s: AccountSort) => s.pk === p.sort)
                .map((s: AccountSort) => s.name)[0]
            : '',
          project_account_d1: state.accountD1List
            ? state.accountD1List
                .filter((d: ProjectAccountD1) => d.pk === p.project_account_d1)
                .map((d: ProjectAccountD1) => d.name)[0]
            : '',
          project_account_d2: state.accountD2List
            ? state.accountD2List
                .filter((d: ProjectAccountD2) => d.pk === p.project_account_d2)
                .map((d: ProjectAccountD2) => d.name)[0]
            : '',
          content: p.content,
          trader: p.trader,
          bank_account: state.proBankAccountList
            ? state.proBankAccountList
                .filter((b: ProjectBankAccount) => b.pk === p.bank_account)
                .map((b: ProjectBankAccount) => b.alias_name)[0]
            : '',
          income: p.income ? p.income : 0,
          outlay: p.outlay ? p.outlay : 0,
          evidence: p.evidence_desc,
        }))
      : []
  },

  proCashPages: (state: ProjectCashState) => (itemsPerPage: number) =>
    Math.ceil(state.proCashesCount / itemsPerPage),
}

export default getters
