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
  // state & getters
  const contract = ref<Contract | null>(null)
  const contractList = ref<Contract[]>([])
  const contractsCount = ref<number>(0)

  const contractor = ref<Contractor | null>(null)
  const contractorList = ref<Contractor[]>([])

  // actions
  const fetchContract = (pk: number) =>
    api
      .get(`/contract-custom-list/${pk}/`)
      .then(res => (contract.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchContractList = (payload: any) => {
    const status = payload.status || '2'
    let apiuri = `/contract-custom-list/?project=${payload.project}&activation=true&contractor__status=${status}`
    if (payload.order_group) apiuri += `&order_group=${payload.order_group}`
    if (payload.unit_type) apiuri += `&unit_type=${payload.unit_type}`
    if (payload.building)
      apiuri += `&keyunit__houseunit__building_unit=${payload.building}`
    if (payload.registed)
      apiuri += `&contractor__is_registed=${payload.registed}`
    if (payload.from_date) apiuri += `&from_contract_date=${payload.from_date}`
    if (payload.to_date) apiuri += `&to_contract_date=${payload.to_date}`
    if (payload.search) apiuri += `&search=${payload.search}`
    const ordering = payload.ordering ? payload.ordering : '-created_at'
    const page = payload.page ? payload.page : 1
    apiuri += `&ordering=${ordering}&page=${page}`

    return api
      .get(apiuri)
      .then(res => {
        contractList.value = res.data.results
        contractsCount.value = res.data.count
      })
      .catch(err => errorHandle(err.response.data))
  }

  // state & getters
  const subsSummaryList = ref<SubsSummary[]>([])
  const contSummaryList = ref<ContractSummary[]>([])

  // actions
  const fetchSubsSummaryList = (project: number) =>
    api
      .get(`/subs-sum/?project=${project}`)
      .then(res => (subsSummaryList.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const fetchContSummaryList = (project: number) =>
    api
      .get(`/cont-sum/?project=${project}`)
      .then(res => (contSummaryList.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const orderGroupList = ref<OrderGroup[]>([])

  const fetchOrderGroupList = (pk: number) =>
    api
      .get(`/order-group/?project=${pk}`)
      .then(res => (orderGroupList.value = res.data))
      .catch(err => errorHandle(err.response.data))

  const createOrderGroup = (payload: OrderGroup) =>
    api
      .post(`/order-group/`, payload)
      .then(res => {
        fetchOrderGroupList(res.data.project).then(() => message())
      })
      .catch(err => errorHandle(err.response.data))

  const updateOrderGroup = (payload: OrderGroup) =>
    api
      .put(`/order-group/${payload.pk}/`, payload)
      .then(res => fetchOrderGroupList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteOrderGroup = (payload: { pk: number; project: number }) =>
    api
      .delete(`/order-group/${payload.pk}/`)
      .then(() =>
        fetchOrderGroupList(payload.project).then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // state & getters
  const keyUnitList = ref<KeyUnit[]>([])
  const houseUnitList = ref<HouseUnit[]>([])
  const salesPriceList = ref<SalesPrice[]>([])
  const downPaymentList = ref<DownPayment[]>([])

  // actions
  const fetchKeyUnitList = (payload: any) => {
    const { project } = payload
    const unit_type = payload.unit_type ? payload.unit_type : ''
    const contract = payload.contract ? payload.contract : ''
    const available = payload.available ? payload.available : 'true'

    return api
      .get(
        `/key-unit/?project=${project}&unit_type=${unit_type}&contract=${contract}&available=${available}`,
      )
      .then(res => (keyUnitList.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }
  const fetchHouseUnitList = (payload: any) => {
    const { project } = payload
    let url = `/available-house-unit/?project=${project}`
    if (payload.unit_type) url += `&unit_type=${payload.unit_type}`
    if (payload.contract) url += `&contract=${payload.contract}`

    return api
      .get(url)
      .then(res => (houseUnitList.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }
  const fetchSalePriceList = (payload: any) => {
    const { project } = payload
    let url = `/price/?project=${project}`
    if (payload.order_group) url += `&order_group=${payload.order_group}`
    if (payload.unit_type) url += `&unit_type=${payload.unit_type}`

    return api
      .get(url)
      .then(res => (salesPriceList.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }
  const fetchDownPayList = (payload: any) => {
    const { project } = payload
    let url = `/down-payment/?project=${project}`
    if (payload.order_group) url += `&order_group=${payload.order_group}`
    if (payload.unit_type) url += `&unit_type=${payload.unit_type}`

    return api
      .get(url)
      .then(res => (downPaymentList.value = res.data))
      .catch(err => errorHandle(err.response.data))
  }

  // state & getters
  const contRelease = ref<ContractRelease | null>(null)
  const contReleaseList = ref<ContractRelease[]>([])
  const contReleaseCount = ref<number>(0)

  // actions
  const fetchContRelease = () => 1
  const fetchContReleaseList = () => 2

  return {
    contract,
    contractList,
    contractsCount,

    contractor,
    contractorList,

    fetchContract,
    fetchContractList,

    subsSummaryList,
    contSummaryList,

    fetchSubsSummaryList,
    fetchContSummaryList,

    orderGroupList,

    fetchOrderGroupList,
    createOrderGroup,
    updateOrderGroup,
    deleteOrderGroup,

    keyUnitList,
    houseUnitList,
    salesPriceList,
    downPaymentList,

    fetchKeyUnitList,
    fetchHouseUnitList,
    fetchSalePriceList,
    fetchDownPayList,

    contRelease,
    contReleaseList,
    contReleaseCount,

    fetchContRelease,
    fetchContReleaseList,
  }
})
