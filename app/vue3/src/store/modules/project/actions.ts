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
import { errorHandle, message } from '@/utils/helper'

const actions = {
  fetchProjectList: ({ commit }: any) => {
    api
      .get('/project/')
      .then(res => {
        commit(FETCH_PROJECT_LIST, res.data)
      })
      .catch(err => errorHandle(err.response.data))
  },

  fetchProject: ({ commit }: any, pk: number) => {
    api
      .get(`/project/${pk}/`)
      .then(res => {
        commit(FETCH_PROJECT, res.data)
      })
      .catch(err => errorHandle(err.response.data))
  },

  createProject: ({ dispatch }: any, payload: any) => {
    api
      .post('/project/', payload)
      .then(res => {
        dispatch('fetchProject', res.data.pk)
        dispatch('fetchProjectList')
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  updateProject: ({ dispatch }: any, payload: any) => {
    api
      .put(`/project/${payload.pk}/`, payload)
      .then(res => {
        dispatch('fetchProject', res.data.pk)
        dispatch('fetchProjectList')
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  deleteProject: ({ dispatch }: any, pk: any) => {
    api
      .delete(`/project/${pk}/`)
      .then(res => {
        console.log(res.data)
        dispatch('fetchProjectList')
        message('danger', '알림!', '삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  },

  fetchTypeList: ({ commit }: any, pk?: number) => {
    api
      .get(`/type/?project=${pk}`)
      .then(res => {
        commit(FETCH_TYPE_LIST, res.data)
      })
      .catch(err => errorHandle(err.response.data))
  },

  createType: ({ dispatch }: any, payload: any) => {
    api
      .post(`/type/`, payload)
      .then(res => {
        dispatch('fetchTypeList', res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  updateType: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/type/${pk}/`, formData)
      .then(res => {
        dispatch('fetchTypeList', res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  deleteType: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/type/${pk}/`)
      .then(() => {
        dispatch('fetchTypeList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  },

  fetchFloorTypeList: ({ commit }: any, pk?: number) => {
    api
      .get(`/floor/?project=${pk}`)
      .then(res => {
        commit(FETCH_FLOOR_TYPE_LIST, res.data)
      })
      .catch(err => errorHandle(err.response.data))
  },

  createFloorType: ({ dispatch }: any, payload: any) => {
    api
      .post(`/floor/`, payload)
      .then(res => {
        dispatch('fetchFloorTypeList', res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  updateFloorType: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/floor/${pk}/`, formData)
      .then(res => {
        dispatch('fetchFloorTypeList', res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  deleteFloorType: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/floor/${pk}/`)
      .then(() => {
        dispatch('fetchFloorTypeList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  },

  fetchBuildingList: ({ commit }: any, pk?: number) => {
    api
      .get(`/bldg/?project=${pk}`)
      .then(res => {
        commit(FETCH_BUILDING_LIST, res.data)
      })
      .catch(err => errorHandle(err.response.data))
  },

  createBuilding: ({ dispatch }: any, payload: any) => {
    api
      .post(`/bldg/`, payload)
      .then(res => {
        dispatch('fetchBuildingList', res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  updateBuilding: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/bldg/${pk}/`, formData)
      .then(res => {
        dispatch('fetchBuildingList', res.data.project)
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  deleteBuilding: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/bldg/${pk}/`)
      .then(() => {
        dispatch('fetchBuildingList', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  },

  fetchHouseUnitList: (
    { commit }: any,
    payload: { project: number; bldg?: number },
  ) => {
    const { project, bldg } = payload
    let urlStr = `/all-house-unit/?project=${project}`
    if (bldg) urlStr += `&building_unit=${bldg}`
    api
      .get(urlStr)
      .then(res => {
        commit(FETCH_HOUSE_UNIT_LIST, res.data)
      })
      .catch(err => errorHandle(err.response.data))
  },

  fetchNumUnitByType: (
    { commit }: any,
    payload: { project: number; unit_type: number },
  ) => {
    const { project, unit_type } = payload
    api
      .get(`/house-unit/?project=${project}&unit_type=${unit_type}`)
      .then(res => {
        commit(FETCH_NUM_UNIT_BY_TYPE, res.data.count)
      })
      .catch(err => errorHandle(err.response.data))
  },

  createUnit: ({ dispatch, getters }: any, payload: any) => {
    const { project, unit_type, ...restPayload } = payload
    const { unit_code, ...unitPayload } = restPayload
    const houseUnits = { ...{ project, unit_type }, ...unitPayload }
    const keyUnits = { project, unit_type, unit_code }
    api
      .post(`/house-unit/`, houseUnits)
      .then(res => {
        dispatch('fetchNumUnitByType', {
          project: res.data.project,
          bldg: res.data.building_unit,
        })
        return api
          .post(`/key-unit/`, keyUnits)
          .catch(err => errorHandle(err.response.data))
      })
      .catch(err => errorHandle(err.response.data))
  },

  updateUnit: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/house-unit/${pk}/`, formData)
      .then(res => {
        dispatch('fetchNumUnitByType', {
          project: res.data.project,
          bldg: res.data.building_unit,
        })
        message()
      })
      .catch(err => errorHandle(err.response.data))
  },

  deleteUnit: ({ dispatch }: any, payload: any) => {
    const { pk, project } = payload
    api
      .delete(`/house-unit/${pk}/`)
      .then(() => {
        dispatch('fetchNumUnitByType', project)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => errorHandle(err.response.data))
  },
}

export default actions
