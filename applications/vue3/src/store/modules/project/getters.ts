import { HouseUnit, Project, ProjectState } from '@/store/modules/project/state'

const getters = {
  projSelect(state: ProjectState) {
    return state.projectList.map((proj: Project) => ({
      value: proj.pk,
      text: proj.name,
    }))
  },

  simpleFloors: (state: ProjectState) =>
    state.floorTypeList.map((f: any) => ({
      pk: f.pk,
      start: f.start_floor,
      end: f.end_floor,
    })),

  unitTable(state: ProjectState) {
    return state.houseUnitList
      ? state.houseUnitList.map((u: HouseUnit) => ({
          color: u.unit_type.color,
          name: u.name,
          line: u.bldg_line,
          floor: u.floor_no,
        }))
      : []
  },
}

export default getters
