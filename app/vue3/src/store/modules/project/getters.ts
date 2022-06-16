import { HouseUnit, Project, ProjectState } from '@/store/modules/project/state'

const getters = {
  allowed_projects: (state: any, getters: any, rootState: any) => {
    return rootState.accounts.userInfo && rootState.accounts.userInfo.staffauth
      ? rootState.accounts.userInfo.staffauth.allowed_projects
      : []
  },

  projSelect: (state: ProjectState, getters: any) =>
    state.projectList
      ? state.projectList
          .filter(x => getters.allowed_projects.includes(x.pk))
          .map((proj: Project) => ({
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
          bldg: u.building_unit,
          color: getters.simpleTypes
            .filter((t: any) => t.pk === u.unit_type)
            .map((t: any) => t.color)[0],
          name: u.name,
          key_unit: u.key_unit,
          line: u.bldg_line,
          floor: u.floor_no,
          is_hold: u.is_hold,
        }))
      : [],

  unitSummary: (state: ProjectState) =>
    state.houseUnitList
      ? {
          totalNum: state.houseUnitList.length,
          holdNum: state.houseUnitList.filter(u => u.is_hold).length,
          appNum: state.houseUnitList.filter(
            u =>
              u.key_unit &&
              u.key_unit.contract &&
              u.key_unit.contract.contractor.status === '1',
          ).length,
          contNum: state.houseUnitList.filter(
            u =>
              u.key_unit &&
              u.key_unit.contract &&
              u.key_unit.contract.contractor.status === '2',
          ).length,
        }
      : { totalNum: 0, holdNum: 0, appNum: 0, contNum: 0 },
}

export default getters
