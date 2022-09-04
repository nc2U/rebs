import api from '@/api'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import {
  Contract,
  Contractor,
  SubsSummary,
  ContractSummary,
  OrderGroup,
  KeyUnit,
  HouseUnit,
  SalesPrice,
  DownPayment,
  ContractRelease,
} from '@/store/types/contract'

export const useContract = defineStore('contract', () => {
  const contract = ref<Contract | null>(null)
  const contractList = ref<Contract[]>([])
  const contractsCount = ref<number>(0)

  const contractor = ref<Contractor | null>(null)
  const contractorList = ref<Contractor[]>([])

  const subsSummaryList = ref<SubsSummary[]>([])
  const contSummaryList = ref<ContractSummary[]>([])

  const orderGroupList = ref<OrderGroup[]>([])
  const keyUnitList = ref<KeyUnit[]>([])
  const houseUnitList = ref<HouseUnit[]>([])
  const salesPriceList = ref<SalesPrice[]>([])
  const downPaymentList = ref<DownPayment[]>([])

  const contRelease = ref<ContractRelease | null>(null)
  const contReleaseList = ref<ContractRelease[]>([])
  const contReleaseCount = ref<number>(0)

  return {
    contract,
    contractList,
    contractsCount,

    contractor,
    contractorList,

    subsSummaryList,
    contSummaryList,

    orderGroupList,
    keyUnitList,
    houseUnitList,
    salesPriceList,
    downPaymentList,

    contRelease,
    contReleaseList,
    contReleaseCount,
  }
})
