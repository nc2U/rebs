import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUnit = defineStore('project', () => {
  // states
  const buildingList = ref([])
  const houseUnitList = ref([])

  const houseUnitNum = ref(0)
  const numUnitByType = ref(0)

  return {
    buildingList,
    houseUnitList,
    houseUnitNum,
    numUnitByType,
  }
})
