import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  UnitType,
  UnitFloorType,
  BuildingUnit,
  HouseUnit,
} from '@/store/types/project'

export const useUnit = defineStore('unit', () => {
  // states
  const unitTypeList = ref<UnitType[]>([])
  const floorTypeList = ref<UnitFloorType[]>([])
  const buildingList = ref<BuildingUnit[]>([])
  const houseUnitList = ref<HouseUnit[]>([])
  const houseUnitNum = ref(0)
  const numUnitByType = ref(0)

  return {
    unitTypeList,
    floorTypeList,
    buildingList,
    houseUnitList,
    houseUnitNum,
    numUnitByType,
  }
})
