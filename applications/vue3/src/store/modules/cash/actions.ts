import api from '@/api'
import { FETCH_PRICE_LIST } from '@/store/modules/cash/mutations-types'
import { message } from '@/utils/helper'
import router from '@/router'

const actions = {
  fetchPriceList: ({ commit }: any, pk?: number) => {
    api
      .get(`/price/?project=${pk}`)
      .then(res => {
        commit(FETCH_PRICE_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  createPrice: ({ dispatch }: any, payload: any) => {
    api
      .post(`/price/`, payload)
      .then(res => {
        dispatch('fetchPriceList', res.data.project)
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

  updatePrice: ({ dispatch }: any, payload: any) => {
    const { pk } = payload
    delete payload.pk
    api
      .put(`/price/${pk}/`, payload)
      .then(res => {
        dispatch('fetchPriceList', res.data.project)
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

  deletePrice: ({ dispatch }: any, payload: any) => {
    const { pk, projId } = payload
    api
      .delete(`/price/${pk}/`)
      .then(() => {
        dispatch('fetchPriceList', projId)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
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
}

export default actions
