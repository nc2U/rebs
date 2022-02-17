import api from '@/api'
import {
  FETCH_BUILDING_LIST,
  FETCH_FLOOR_TYPE_LIST,
  FETCH_HOUSE_UNIT_LIST,
  FETCH_NUM_UNIT_BY_TYPE,
  FETCH_PROJECT,
  FETCH_PROJECT_LIST,
  FETCH_TYPE_LIST,
} from '@/store/modules/project/mutations-types'
import { message } from '@/utils/helper'

const actions = {
  fetchProjectList: ({ commit }: any) => {
    api
      .get('/project/')
      .then(res => {
        commit(FETCH_PROJECT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchProject: ({ commit }: any, pk: number) => {
    api
      .get(`/project/${pk}/`)
      .then(res => {
        commit(FETCH_PROJECT, res.data)
      })
      .catch(err => console.log(err.response.data))
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
      .catch(err => console.log(err.response.data))
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
    const { pk, ...formData } = payload
    api
      .put(`/type/${pk}/`, formData)
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
    const { pk, project } = payload
    api
      .delete(`/type/${pk}/`)
      .then(() => {
        dispatch('fetchTypeList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => {
        alert(
          '해당 그룹에 종속된 계약관련 데이터가 있는 경우 이 그룹을 삭제할 수 없습니다.',
        )
      })
  },

  fetchFloorTypeList: ({ commit }: any, pk?: number) => {
    api
      .get(`/floor/?project=${pk}`)
      .then(res => {
        commit(FETCH_FLOOR_TYPE_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
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
    const { pk, ...formData } = payload
    api
      .put(`/floor/${pk}/`, formData)
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
    const { pk, project } = payload
    api
      .delete(`/floor/${pk}/`)
      .then(() => {
        dispatch('fetchFloorTypeList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(() => {
        alert(
          '해당 그룹에 종속된 분양가 데이터가 있는 경우 이 그룹을 삭제할 수 없습니다.',
        )
      })
  },

  fetchBuildingList: ({ commit }: any, pk?: number) => {
    api
      .get(`/bldg/?project=${pk}`)
      .then(res => {
        commit(FETCH_BUILDING_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  createBuilding: ({ dispatch }: any, payload: any) => {
    api
      .post(`/bldg/`, payload)
      .then(res => {
        dispatch('fetchBuildingList', res.data.project)
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

  updateBuilding: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/bldg/${pk}/`, formData)
      .then(res => {
        dispatch('fetchBuildingList', res.data.project)
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

  deleteBuilding: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/bldg/${pk}/`)
      .then(() => {
        dispatch('fetchBuildingList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(() => {
        alert(
          '해당 그룹에 종속된 호수(Unit) 관련 데이터가 있는 경우 이 그룹을 삭제할 수 없습니다.',
        )
      })
  },

  fetchUnitList: (
    { commit }: any,
    payload: { project: number; bldg: number },
  ) => {
    const { project, bldg } = payload
    const urlStr = `/unit/?project=${project}&building_unit=${bldg}`
    api
      .get(urlStr)
      .then(res => {
        commit(FETCH_HOUSE_UNIT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchNumUnitByType: (
    { commit }: any,
    payload: { project: number; unit_type: number },
  ) => {
    const { project, unit_type } = payload
    api
      .get(`/unit/?project=${project}&unit_type=${unit_type}`)
      .then(res => {
        commit(FETCH_NUM_UNIT_BY_TYPE, res.data.count)
      })
      .catch(err => console.log(err.response.data))
  },

  createUnit: ({ dispatch }: any, payload: any) => {
    api
      .post(`/unit/`, payload)
      .then(res => {
        dispatch('fetchUnitList', res.data.project)
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

  updateUnit: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/unit/${pk}/`, formData)
      .then(res => {
        dispatch('fetchUnitList', res.data.project)
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

  deleteUnit: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/unit/${pk}/`)
      .then(() => {
        dispatch('fetchUnitList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(() => {
        alert(
          '해당 그룹에 종속된 계약관련 데이터가 있는 경우 이 그룹을 삭제할 수 없습니다.',
        )
      })
  },
}

export default actions
