<script lang="ts" setup>
import { ref, computed, PropType } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import { SimpleUnit } from './ContractBoard.vue'
import Unit from '@/views/contracts/Status/components/Unit.vue'

const props = defineProps({
  bldg: { type: Number, default: null },
  maxFloor: { type: Number, default: null },
  units: { type: Object as PropType<SimpleUnit[]>, default: null },
})

const maxPiloti = ref(3) // 맥스 피로티 층

const pDataStore = useProjectData()
const buildingList = computed(() => pDataStore.buildingList)
const lineList = computed(() => {
  const lines = [...new Set(props.units.map((u: { line: number }) => u.line))] as number[]
  return lines.sort((prev: number, curr: number) => prev - curr)
})
const floorList = computed(() => {
  const floors = [...new Set(props.units.map((u: { floor: number }) => u.floor))] as number[]
  return floors.sort((prev: number, curr: number) => curr - prev)
})
const bldgWidth = computed(() => 40 * lineList.value.length)

const getUnit = (line: number, floor: number) =>
  props.units
    .filter((u: { line: number }) => u.line === line)
    .filter((u: { floor: number }) => u.floor === floor)[0]

const getFirst = (floor: number) =>
  floor > maxPiloti.value
    ? props.units
        .filter((u: { floor: number }) => u.floor == floor)
        .map((u: { line: number }) => u.line)
        .sort()[0]
    : 1

const bldgName = (bldg: number) =>
  buildingList.value.filter((b: { pk: number; name: string }) => b.pk === bldg).map(b => b.name)[0]
</script>

<template>
  <CCol class="ml-4 mt-5" :style="{ width: `${bldgWidth}px` }">
    <CRow v-for="i in floorList as Array<number>" :key="i" :style="{ width: `${bldgWidth}px` }">
      <Unit
        v-for="line in lineList as number[]"
        :key="line"
        :units="units"
        :unit="getUnit(line, i)"
        :floor="i"
        :line="line"
        :max-piloti="maxPiloti"
        :first-line="getFirst(i)"
      />
    </CRow>
    <CRow :style="{ width: `${bldgWidth}px` }">
      <CCol class="text-center build-base">
        <strong>{{ bldgName(bldg) }} 동</strong>
      </CCol>
    </CRow>
  </CCol>
</template>

<style lang="scss" scoped>
.build-base {
  height: 36px;
  background: #666;
  color: white;
  line-height: 36px;
  vertical-align: middle;
  border: solid #555 1px;
}

.dark-theme {
  .build-base {
    background: #333;
  }
}
</style>
