import {
  FETCH_PROJECT,
  FETCH_PROJECT_LIST,
} from '@/store/modules/project/mutations-types'
import { Project, ProjectState } from '@/store/modules/project/state'

const mutations = {
  [FETCH_PROJECT_LIST]: (state: ProjectState, payload: any) => {
    state.projectList = payload.results
  },

  [FETCH_PROJECT]: (state: ProjectState, payload: Project) => {
    state.project = payload
  },
}

export default mutations
