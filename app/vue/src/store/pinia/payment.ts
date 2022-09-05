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

export const usePayment = defineStore('payment', () => {
  // state & getters
})
