import api from '@/api'
import {
  FETCH_CONTRACT,
  FETCH_CONTRACT_LIST,
  FETCH_ORDER_GROUP_LIST,
  FETCH_SUBS_SUMMARY_LIST,
  FETCH_CONT_SUMMARY_LIST,
} from '@/store/modules/contract/mutations-types'
import router from '@/router'
import { message } from '@/utils/helper'

const actions = {
  fetchContractList: ({ commit }: any, payload?: any) => {
    const { project } = payload
    const status = payload.status ? payload.status : '2'
    let url = `/contract/?project=${project}&activation=true&contractor__status=${status}`
    if (payload.order_group) url += `&order_group=${payload.order_group}`
    if (payload.unit_type) url += `&unit_type=${payload.unit_type}`
    if (payload.building)
      url += `&keyunit__houseunit__building_unit=${payload.building}`
    if (payload.registed) url += `&contractor__is_registed=${payload.registed}`
    if (payload.from_date) url += `&from_contract_date=${payload.from_date}`
    if (payload.to_date) url += `&to_contract_date=${payload.to_date}`
    if (payload.ordering) url += `&ordering=${payload.ordering}`
    if (payload.search) url += `&search=${payload.search}`
    const page = payload.page ? payload.page : 1
    url += `&page=${page}`

    api
      .get(url)
      .then(res => {
        commit(FETCH_CONTRACT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchContract: ({ commit }: any, pk: number) => {
    api
      .get(`/contract/${pk}/`)
      .then(res => {
        commit(FETCH_CONTRACT, res.data)
      })
      .catch(console.log)
  },

  fetchSubsSummaryList: ({ commit }: any, project?: number) => {
    api
      .get(`/subs-sum/?project=${project}`)
      .then(res => {
        commit(FETCH_SUBS_SUMMARY_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchContSummaryList: ({ commit }: any, project?: number) => {
    api
      .get(`/cont-sum/?project=${project}`)
      .then(res => {
        commit(FETCH_CONT_SUMMARY_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchOrderGroupList: ({ commit }: any, pk?: number) => {
    api
      .get(`/order-group/?project=${pk}`)
      .then(res => {
        commit(FETCH_ORDER_GROUP_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  createOrderGroup: ({ dispatch }: any, payload: any) => {
    api
      .post(`/order-group/`, payload)
      .then(res => {
        dispatch('fetchOrderGroupList', res.data.project)
        message()
      })
      .catch(err => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },

  updateOrderGroup: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/order-group/${pk}/`, formData)
      .then(res => {
        dispatch('fetchOrderGroupList', res.data.project)
        message()
      })
      .catch(err => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },

  deleteOrderGroup: ({ dispatch }: any, payload: any) => {
    const { pk, projId } = payload
    api
      .delete(`/order-group/${pk}/`)
      .then(() => {
        dispatch('fetchOrderGroupList', projId)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => {
        alert(
          '해당 그룹에 종속된 계약관련 데이터가 있는 경우 이 그룹을 삭제할 수 없습니다.',
        )
        ;(router as any).go()
      })
  },
}

export default actions
