import {
  FETCH_PROJECT_LIST,
  FETCH_PROJECT,
  FETCH_TYPE_LIST,
  FETCH_FLOOR_TYPE_LIST,
  FETCH_BUILDING_LIST,
  FETCH_HOUSE_UNIT_LIST,
  FETCH_NUM_UNIT_BY_TYPE,
} from '@/store/modules/project/mutations-types'
import { Project, ProjectState } from '@/store/modules/project/state'

const mutations = {
  [FETCH_PROJECT_LIST]: (state: ProjectState, payload: any) => {
    state.projectList = payload.results
  },

  [FETCH_PROJECT]: (state: ProjectState, payload: Project) => {
    state.project = payload
  },

  [FETCH_TYPE_LIST]: (state: ProjectState, payload: any) => {
    state.unitTypeList = payload.results
  },

  [FETCH_FLOOR_TYPE_LIST]: (state: ProjectState, payload: any) => {
    state.floorTypeList = payload.results
  },

  [FETCH_BUILDING_LIST]: (state: ProjectState, payload: any) => {
    state.buildingList = payload.results
  },

  [FETCH_HOUSE_UNIT_LIST]: (state: ProjectState, payload: any) => {
    state.houseUnitList = payload.results
  },

  [FETCH_NUM_UNIT_BY_TYPE]: (state: ProjectState, count: number) => {
    state.numUnitByType = count
  },
}

export default mutations
