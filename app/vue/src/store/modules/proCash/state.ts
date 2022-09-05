import { State } from '@/store'
import { AccountSort } from '@/store/modules/comCash/state'
import {
  ProjectAccountD1,
  ProjectAccountD2,
  ProjectBankAccount,
  BalanceByAccount,
  ProjectCashBook,
  ProjectBudget,
  ExecAmountToBudget,
} from '@/store/types/proCash'

export interface ProjectCashState extends State {
  sortList: AccountSort[]
  allAccD1List: ProjectAccountD1[]
  allAccD2List: ProjectAccountD2[]
  formAccD1List: ProjectAccountD1[]
  formAccD2List: ProjectAccountD2[]
  proBankAccountList: ProjectBankAccount[]
  balanceByAccList: BalanceByAccount[]
  proDateCashBook: ProjectCashBook[]
  proBudgetList: ProjectBudget[]
  execAmountList: ExecAmountToBudget[]
  proCashBookList: ProjectCashBook[]
  proCashesCount: number
  proImprestList: ProjectCashBook[]
  proImprestCount: number
}

const state = {
  sortList: [],
  allAccD1List: [],
  allAccD2List: [],
  formAccD1List: [],
  formAccD2List: [],
  proBankAccountList: [],
  balanceByAccList: [],
  proDateCashBook: [],
  proBudgetList: [],
  execAmountList: [],
  proCashBookList: [],
  proCashesCount: 0,
  proImprestList: [],
  proImprestCount: 0,
}

export default state
