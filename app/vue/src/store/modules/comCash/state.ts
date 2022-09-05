import { State } from '@/store'
import {
  AccountSort,
  AccountD1,
  AccountD2,
  AccountD3,
  CompanyBank,
  BalanceByAccount,
  CashBook,
} from '@/store/types/comCash'

export interface CashesState extends State {
  sortList: AccountSort[]
  formAccD1List: AccountD1[]
  formAccD2List: AccountD2[]
  formAccD3List: AccountD3[]
  listAccD1List: AccountD1[]
  listAccD2List: AccountD2[]
  listAccD3List: AccountD3[]
  comBankList: CompanyBank[]
  comBalanceByAccList: BalanceByAccount[]
  dateCashBook: CashBook[]
  cashBookList: CashBook[]
  cashBookCount: number
}

const state = {
  sortList: [],
  formAccD1List: [],
  formAccD2List: [],
  formAccD3List: [],
  listAccD1List: [],
  listAccD2List: [],
  listAccD3List: [],
  comBankList: [],
  comBalanceByAccList: [],
  dateCashBook: [],
  cashBookList: [],
  cashBookCount: 0,
}

export default state
