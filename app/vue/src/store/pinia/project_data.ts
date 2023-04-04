import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import {
  UnitType,
  UnitFloorType,
  BuildingUnit,
  HouseUnit,
} from '@/store/types/project'
import api from '@/api'
import { errorHandle, message } from '@/utils/helper'

export type CreateUnit = {
  project: number
  unit_type: number
  building_unit: number
  bldg_line: number
  floor_no: number
  name: string
  floor_type: number
  unit_code: string
}

export const useProjectData = defineStore('projectData', () => {
  // states & getters
  const unitTypeList = ref<UnitType[]>([])
  const simpleTypes = computed(() =>
    unitTypeList.value
      ? unitTypeList.value.map((t: UnitType) => ({
          pk: t.pk,
          name: t.name,
          color: t.color,
        }))
      : [],
  )
  const getTypes = computed(() =>
    unitTypeList.value.map(t => ({
      value: t.pk,
      label: t.name,
    })),
  )

  // actions
  const fetchTypeList = (projId: number) =>
    api
      .get(`/type/?project=${projId}`)
      .then(res => {
        unitTypeList.value = res.data.results
      })
      .catch(err => errorHandle(err.response.data))

  const createType = (payload: UnitType) =>
    api
      .post(`/type/`, payload)
      .then(res => fetchTypeList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const updateType = (payload: UnitType) =>
    api
      .put(`/type/${payload.pk}/`, payload)
      .then(res => fetchTypeList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteType = (pk: number, project: number) =>
    api
      .delete(`/type/${pk}/`)
      .then(() =>
        fetchTypeList(project).then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // states & getters
  const floorTypeList = ref<UnitFloorType[]>([])
  const simpleFloors = computed(() =>
    floorTypeList.value
      ? floorTypeList.value.map((f: UnitFloorType) => ({
          pk: f.pk,
          start: f.start_floor,
          end: f.end_floor,
          name: f.alias_name,
        }))
      : [],
  )
  const getFloorTypes = computed(() =>
    floorTypeList.value.map(f => ({ valume: f.pk, label: f.alias_name })),
  )

  // actions
  const fetchFloorTypeList = (projId: number) =>
    api
      .get(`/floor/?project=${projId}`)
      .then(res => (floorTypeList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createFloorType = (payload: UnitFloorType) =>
    api
      .post(`/floor/`, payload)
      .then(res => fetchFloorTypeList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const updateFloorType = (payload: UnitFloorType) =>
    api
      .put(`/floor/${payload.pk}/`, payload)
      .then(res => fetchFloorTypeList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteFloorType = (pk: number, project: number) =>
    api
      .delete(`/floor/${pk}/`)
      .then(() =>
        fetchFloorTypeList(project).then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // states & getters
  const buildingList = ref<BuildingUnit[]>([])

  // actions
  const fetchBuildingList = (projId: number) =>
    api
      .get(`/bldg/?project=${projId}`)
      .then(res => (buildingList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createBuilding = (payload: BuildingUnit) =>
    api
      .post(`/bldg/`, payload)
      .then(res => fetchBuildingList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const updateBuilding = (payload: BuildingUnit) =>
    api
      .put(`/bldg/${payload.pk}/`, payload)
      .then(res => fetchBuildingList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteBuilding = (pk: number, project: number) =>
    api
      .delete(`/bldg/${pk}/`)
      .then(() =>
        fetchBuildingList(project).then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  // states & getters
  const houseUnitList = ref<HouseUnit[]>([])
  const houseUnitNum = ref(0)
  const simpleUnits = computed(() =>
    houseUnitList.value
      ? houseUnitList.value.map((u: HouseUnit) => ({
          bldg: u.building_unit,
          color: simpleTypes.value
            .filter((t: { pk: number }) => t.pk === u.unit_type)
            .map((t: { color: string }) => t.color)[0],
          name: u.name,
          key_unit: u.key_unit,
          line: u.bldg_line,
          floor: u.floor_no,
          is_hold: u.is_hold,
        }))
      : [],
  )
  const unitSummary = computed(() =>
    houseUnitList.value
      ? {
          totalNum: houseUnitList.value.length,
          holdNum: houseUnitList.value.filter(u => u.is_hold).length,
          appNum: houseUnitList.value.filter(
            u =>
              u.key_unit &&
              u.key_unit.contract &&
              u.key_unit.contract.contractor.status === '1',
          ).length,
          contNum: houseUnitList.value.filter(
            u =>
              u.key_unit &&
              u.key_unit.contract &&
              u.key_unit.contract.contractor.status === '2',
          ).length,
        }
      : { totalNum: 0, holdNum: 0, appNum: 0, contNum: 0 },
  )
  const numUnitByType = ref(0)

  // actions
  const fetchHouseUnitList = (project: number, bldg?: number) => {
    let apiUri = `/all-house-unit/?building_unit__project=${project}`
    if (bldg) apiUri += `&building_unit=${bldg}`
    return api
      .get(apiUri)
      .then(res => (houseUnitList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const fetchNumUnitByType = (project: number, unit_type: number) =>
    api
      .get(
        `/house-unit/?building_unit__project=${project}&unit_type=${unit_type}`,
      )
      .then(res => (numUnitByType.value = res.data.count))
      .catch(err => errorHandle(err.response.data))

  const createUnit = (payload: CreateUnit) => {
    const { project, unit_type, ...restPayload } = payload
    const { unit_code, ...unitPayload } = restPayload
    const houseUnits = { ...{ project, unit_type }, ...unitPayload }
    const keyUnits = { project, unit_type, unit_code }
    api
      .post(`/house-unit/`, houseUnits)
      .then(() =>
        fetchNumUnitByType(project, unit_type).then(() =>
          api
            .post(`/key-unit/`, keyUnits)
            .catch(err => errorHandle(err.response.data)),
        ),
      )
      .catch(err => errorHandle(err.response.data))
  }

  const updateUnit = (payload: HouseUnit) =>
    api
      .put(`/house-unit/${payload.pk}/`, payload)
      .then(res =>
        fetchNumUnitByType(res.data.project, res.data.building_unit).then(() =>
          message(),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const deleteUnit = (pk: number, project: number, unit_type: number) =>
    api
      .delete(`/house-unit/${pk}/`)
      .then(() =>
        fetchNumUnitByType(project, unit_type).then(() =>
          message('warning', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  return {
    unitTypeList,
    simpleTypes,
    getTypes,
    fetchTypeList,
    createType,
    updateType,
    deleteType,

    floorTypeList,
    simpleFloors,
    getFloorTypes,
    fetchFloorTypeList,
    createFloorType,
    updateFloorType,
    deleteFloorType,

    buildingList,
    fetchBuildingList,
    createBuilding,
    updateBuilding,
    deleteBuilding,

    houseUnitList,
    houseUnitNum,
    simpleUnits,
    unitSummary,
    numUnitByType,
    fetchHouseUnitList,
    fetchNumUnitByType,
    createUnit,
    updateUnit,
    deleteUnit,
  }
})
