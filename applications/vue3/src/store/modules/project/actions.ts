import api from '@/api'
import {
  FETCH_FLOOR_TYPE_LIST,
  FETCH_PROJECT,
  FETCH_PROJECT_LIST,
  FETCH_TYPE_LIST,
} from '@/store/modules/project/mutations-types'
import { message } from '@/utils/helper'
import router from '@/router'

const actions = {
  fetchProjectList: ({ commit }: any) => {
    api
      .get('/project/')
      .then(res => {
        commit(FETCH_PROJECT_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  fetchProject: ({ commit }: any, pk: number) => {
    api
      .get(`/project/${pk}/`)
      .then(res => {
        commit(FETCH_PROJECT, res.data)
      })
      .catch(err => console.log(err))
  },

  createProject: ({ dispatch }: any, payload: any) => {
    api
      .post('/project/', payload)
      .then(res => {
        dispatch('fetchProject', res.data.pk)
        dispatch('fetchProjectList')
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

  updateProject: ({ dispatch }: any, payload: any) => {
    api
      .put(`/project/${payload.pk}/`, payload)
      .then(res => {
        dispatch('fetchProject', res.data.pk)
        dispatch('fetchProjectList')
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

  deleteProject: ({ dispatch }: any, pk: any) => {
    api.delete(`/project/${pk}/`).then(res => {
      console.log(res.data)
      dispatch('fetchProjectList')
      message('danger', '알림!', '삭제되었습니다.')
    })
  },

  fetchTypeList: ({ commit }: any, pk?: number) => {
    api
      .get(`/type/?project=${pk}`)
      .then(res => {
        commit(FETCH_TYPE_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  createType: ({ dispatch }: any, payload: any) => {
    api
      .post(`/type/`, payload)
      .then(res => {
        dispatch('fetchTypeList', res.data.project)
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

  updateType: ({ dispatch }: any, payload: any) => {
    const { pk } = payload
    delete payload.pk
    api
      .put(`/type/${pk}/`, payload)
      .then(res => {
        dispatch('fetchTypeList', res.data.project)
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

  deleteType: ({ dispatch }: any, payload: any) => {
    const { pk, projId } = payload
    api
      .delete(`/type/${pk}/`)
      .then(() => {
        dispatch('fetchTypeList', projId)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => {
        alert(
          '해당 그룹에 종속된 계약관련 데이터가 있는 경우 이 그룹을 삭제할 수 없습니다.',
        )
        ;(router as any).go()
      })
  },

  fetchFloorTypeList: ({ commit }: any, pk?: number) => {
    api
      .get(`/floor/?project=${pk}`)
      .then(res => {
        commit(FETCH_FLOOR_TYPE_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  createFloorType: ({ dispatch }: any, payload: any) => {
    api
      .post(`/floor/`, payload)
      .then(res => {
        dispatch('fetchFloorTypeList', res.data.project)
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

  updateFloorType: ({ dispatch }: any, payload: any) => {
    const { pk } = payload
    delete payload.pk
    api
      .put(`/floor/${pk}/`, payload)
      .then(res => {
        dispatch('fetchFloorTypeList', res.data.project)
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

  deleteFloorType: ({ dispatch }: any, payload: any) => {
    const { pk, projId } = payload
    api
      .delete(`/floor/${pk}/`)
      .then(() => {
        dispatch('fetchFloorTypeList', projId)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(() => {
        alert(
          '해당 그룹에 종속된 분양가 데이터가 있는 경우 이 그룹을 삭제할 수 없습니다.',
        )
        ;(router as any).go()
      })
  },
}

export default actions
