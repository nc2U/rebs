import api from '@/api'
import {
  FETCH_PROJECT,
  FETCH_PROJECT_LIST,
} from '@/store/modules/project/mutations-types'
import { message } from '@/utils/helper'

const actions = {
  fetchProjectList: ({ commit }: any) => {
    api
      .get('/project/')
      .then((res) => {
        commit(FETCH_PROJECT_LIST, res.data.results)
      })
      .catch((err) => console.log(err))
  },

  fetchProject: ({ commit }: any, pk: { pk: string }) => {
    api
      .get(`/project/${pk}/`)
      .then((res) => {
        commit(FETCH_PROJECT, res.data)
      })
      .catch((err) => console.log(err))
  },

  createProject: ({ dispatch }: any, payload: any) => {
    api
      .post('/project/', payload)
      .then((res) => {
        dispatch('fetchProject', res.data.id)
        dispatch('fetchProjectList')
        message()
      })
      .catch((err) => alert(err.response.data.detail))
  },

  updateProject: ({ dispatch }: any, payload: any) => {
    api
      .put(`/project/${payload.pk}/`, payload)
      .then((res) => {
        dispatch('fetchProject', res.data.pk)
        dispatch('fetchProjectList')
        message()
      })
      .catch((err) => alert(err.response.data.detail))
  },

  deleteProject: ({ dispatch }: any, pk: any) => {
    api.delete(`/project/${pk}/`).then((res) => {
      console.log(res.data)
      dispatch('fetchProjectList')
      message('danger', '알림!', '삭제되었습니다.')
    })
  },
}

export default actions
