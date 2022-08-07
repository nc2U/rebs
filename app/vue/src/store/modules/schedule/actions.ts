import api from '@/api'
import updateState from './mutations'
import { errorHandle, message } from '@/utils/helper'

const actions = {
  fetchScheduleList: ({ commit }: any) => {
    api
      .get('/schedule/')
      .then(res => {
        commit(updateState, res.data)
      })
      .catch(err => errorHandle(err.response.data))
  },

  fetchSchedule: ({ commit }: any, payload: any) => {
    const { pk } = payload
    api
      .get(`/schedule/${pk}/`)
      .then(res => {
        commit(updateState, res.data)
      })
      .catch(err => errorHandle(err.response.data))
  },

  createSchedule: ({ dispatch }: any, payload: any) => {
    api
      .post('/schedule/', payload)
      .then(res => {
        dispatch('fetchSchedule', res.data.pk)
        dispatch('fetchScheduleList')
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  patchSchedule: ({ dispatch }: any, payload: any) => {
    const { pk, ...data } = payload
    api
      .patch(`/schedule/${pk}`, data)
      .then(res => {
        dispatch('fetchSchedule', res.data.pk)
        dispatch('fetchScheduleList')
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  updateSchedule: ({ dispatch }: any, payload: any) => {
    const { pk, ...data } = payload
    api
      .put(`/schedule/${pk}`, data)
      .then(res => {
        dispatch('fetchSchedule', res.data.pk)
        dispatch('fetchScheduleList')
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  deleteSchedule: ({ dispatch }: any, pk: number) => {
    api
      .delete(`/schedule/${pk}`)
      .then(res => {
        dispatch('fetchScheduleList')
        console.log(res.data)
        message('danger', '알림!', '삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  },
}

export default actions
