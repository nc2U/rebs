import api from '@/api'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import {
  Price,
  PayOrder,
  DownPay,
  PaySumByType,
  ContractNum,
} from '@/store/types/payment'
import { ProjectCashBook } from '@/store/types/proCash'

export const usePayment = defineStore('payment', () => {
  // state & getters
  const priceList = ref<Price[]>([])
  const payOrderList = ref<PayOrder[]>([])
  const payOrder = ref<PayOrder | null>(null)
  const downPayList = ref<DownPay[]>([])
  const paymentList = ref<ProjectCashBook[]>([])
  const AllPaymentList = ref<ProjectCashBook[]>([])
  const paymentsCount = ref<number>(0)
  const paySumList = ref<PaySumByType[]>([])
  const contNumList = ref<ContractNum[]>([])

  return {
    priceList,
    payOrderList,
    payOrder,
    downPayList,
    paymentList,
    AllPaymentList,
    paymentsCount,
    paySumList,
    contNumList,
  }
})
