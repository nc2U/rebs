import { State } from '@/store'
import { ProjectCashBook } from '@/store/types/proCash'
import {
  Price,
  PayOrder,
  DownPay,
  PaySumByType,
  ContractNum,
} from '@/store/types/payment'

export interface PaymentState extends State {
  priceList: Price[]
  payOrderList: PayOrder[]
  payOrder: PayOrder | null
  downPayList: DownPay[]
  paymentList: ProjectCashBook[]
  AllPaymentList: ProjectCashBook[]
  paymentsCount: number
  paySumList: PaySumByType[]
  contNumList: ContractNum[]
}

const state: PaymentState = {
  priceList: [],
  payOrderList: [],
  payOrder: null,
  downPayList: [],
  paymentList: [],
  AllPaymentList: [],
  paymentsCount: 0,
  paySumList: [],
  contNumList: [],
}

export default state
