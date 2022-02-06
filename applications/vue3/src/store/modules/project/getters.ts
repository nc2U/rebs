import { Project, ProjectState } from '@/store/modules/project/state'

const getters = {
  projSelect(state: ProjectState) {
    return state.projectList.map((proj: Project) => ({
      value: proj.pk,
      text: proj.name,
    }))
  },
}

export default getters
