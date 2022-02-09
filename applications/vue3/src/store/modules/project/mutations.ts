import {
  FETCH_FLOOR_TYPE_LIST,
  FETCH_PROJECT,
  FETCH_PROJECT_LIST,
  FETCH_TYPE_LIST,
  FETCH_TYPE,
} from '@/store/modules/project/mutations-types'
import { Project, ProjectState, UnitType } from '@/store/modules/project/state'

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

  [FETCH_TYPE]: (state: ProjectState, payload: UnitType) => {
    state.unitType = payload
  },

  [FETCH_FLOOR_TYPE_LIST]: (state: ProjectState, payload: any) => {
    state.floorTypeList = payload.results
  },
}

export default mutations
