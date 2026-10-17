<script lang="ts" setup>
import { computed } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import LazyBuilding from '@/views/contracts/Status/components/LazyBuilding.vue'

import { type KeyUnit } from '@/store/types/project'

export type SimpleUnit = {
  bldg: number
  color: string
  name: string
  key_unit: KeyUnit
  line: number
  floor: number
  is_hold: boolean
  hold_reason: string
}

const pDataStore = useProjectData()
const simpleUnits = computed(() => pDataStore.simpleUnits)

// 숫자 오름차순 정렬 (기본 .sort()의 문자열 사전순 정렬 버그 수정)
const getBldg = computed(() =>
  [...new Set(simpleUnits.value.map((u: SimpleUnit) => u.bldg))].sort((a, b) => a - b),
)

// 빌딩별 유닛 사전 그룹화 캐싱 (매 렌더링 시 filter 호출 제거)
const unitsByBuilding = computed(() => {
  const map = new Map<number, SimpleUnit[]>()
  for (const u of simpleUnits.value) {
    const list = map.get(u.bldg)
    if (list) {
      list.push(u)
    } else {
      map.set(u.bldg, [u])
    }
  }
  return map
})

const maxFloor = computed(() => {
  if (!simpleUnits.value.length) return 0
  return Math.max(...simpleUnits.value.map((u: SimpleUnit) => u.floor))
})

const getUnits = (bldg: number): SimpleUnit[] => unitsByBuilding.value.get(bldg) || []
</script>

<template>
  <CRow v-if="simpleUnits.length === 0">
    <CCol class="text-center p-5 text-danger"> 등록된 데이터가 없습니다.</CCol>
  </CRow>

  <div v-else class="buildings-container">
    <LazyBuilding
      v-for="bldg in getBldg"
      :key="bldg"
      :bldg="bldg"
      :max-floor="maxFloor"
      :units="getUnits(bldg)"
    />
  </div>
</template>

<style scoped>
.buildings-container {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 1rem;
  max-width: 100%;
  overflow-x: auto;
}
</style>
