import { HouseUnit, Project, ProjectState } from '@/store/modules/project/state'

const getters = {
  projSelect(state: ProjectState) {
    return state.projectList.map((proj: Project) => ({
      value: proj.pk,
      text: proj.name,
    }))
  },

  unitTable(state: ProjectState) {
    return state.houseUnitList
      ? state.houseUnitList.map((u: HouseUnit) => ({
          color: u.unit_type.color,
          name: u.name,
          line: u.bldg_line,
          floor: u.floor_no,
          is_hold: u.is_hold,
        }))
      : []
  },
}

export default getters
