import api from '@/api'
import {
  FETCH_CONTRACT,
  FETCH_CONTRACT_LIST,
  FETCH_ORDER_GROUP_LIST,
} from '@/store/modules/contract/mutations-types'
import router from '@/router'
import { message } from '@/utils/helper'

const actions = {
  fetchContractList: ({ commit }: any, payload?: any) => {
    const { project } = payload
    const order_group = payload.order_group ? payload.order_group : ''
    const page = payload.page ? payload.page : 1
    api
      .get(
        `/contract/?project=${project}&order_group=${order_group}&activation=true&page=${page}`,
      )
      .then(res => {
        commit(FETCH_CONTRACT_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  fetchContract: ({ commit }: any, pk: number) => {
    api
      .get(`/contract/${pk}/`)
      .then(res => {
        commit(FETCH_CONTRACT, res.data)
      })
      .catch(err => console.log(err))
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
    const { pk } = payload
    delete payload.pk
    api
      .put(`/order-group/${pk}/`, payload)
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
