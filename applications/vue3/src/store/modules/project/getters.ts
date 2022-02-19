import { HouseUnit, Project, ProjectState } from '@/store/modules/project/state'

const getters = {
  projSelect: (state: ProjectState) =>
    state.projectList
      ? state.projectList.map((proj: Project) => ({
          value: proj.pk,
          text: proj.name,
        }))
      : [],

  simpleTypes: (state: ProjectState) =>
    state.unitTypeList
      ? state.unitTypeList.map((t: any) => ({
          pk: t.pk,
          name: t.name,
          color: t.color,
        }))
      : [],

  simpleFloors: (state: ProjectState) =>
    state.floorTypeList
      ? state.floorTypeList.map((f: any) => ({
          pk: f.pk,
          start: f.start_floor,
          end: f.end_floor,
          name: f.alias_name,
        }))
      : [],

  simpleUnits: (state: ProjectState, getters: any) =>
    state.houseUnitList
      ? state.houseUnitList.map((u: HouseUnit) => ({
          color: getters.simpleTypes
            .filter((t: any) => t.pk === u.unit_type)
            .map((t: any) => t.color)[0],
          name: u.name,
          line: u.bldg_line,
          floor: u.floor_no,
        }))
      : [],
}

export default getters
