<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import Unit from '@/views/contracts/Status/components/Unit.vue'

const props = defineProps({
  bldg: { type: Number, default: null },
  maxFloor: { type: Number, default: null },
  units: { type: Object, default: null },
})

const maxPiloti = ref(3) // 맥스 피로티 층

const pDataStore = useProjectData()
const buildingList = computed(() => pDataStore.buildingList)
const lineList = computed(() =>
  [...new Set(props.units.map((u: { line: number }) => u.line))].sort(
    (a: any, b: any) => a - b,
  ),
)
const floorList = computed(() =>
  [...new Set(props.units.map((u: { floor: number }) => u.floor))].sort(
    (a: any, b: any) => b - a,
  ),
)

const getUnit = (line: number, floor: number) =>
  props.units
    .filter((u: { line: number }) => u.line === line)
    .filter((u: { floor: number }) => u.floor === floor)[0]

const getFirst = (line: number, floor: number) =>
  floor > maxPiloti.value
    ? props.units
        .filter((u: { floor: number }) => u.floor == floor)
        .map((u: { line: number }) => u.line)
        .sort()[0]
    : 1

const bldgName = (bldg: number) =>
  buildingList.value
    .filter((b: { pk: number; name: string }) => b.pk === bldg)
    .map(b => b.name)[0]
</script>

<template>
  <CCol class="ml-4 mt-5">
    <CRow v-for="i in floorList" :key="i">
      <Unit
        v-for="line in lineList"
        :key="line"
        :units="units"
        :unit="getUnit(line, i)"
        :floor="i"
        :line="line"
        :max-piloti="maxPiloti"
        :first-line="getFirst(line, i)"
      />
    </CRow>
    <CRow v-if="lineList">
      <div
        class="text-center build-base"
        :style="{
          width: `${40 * lineList.length}px`,
        }"
      >
        <strong>{{ bldgName(bldg) }} 동</strong>
      </div>
    </CRow>
  </CCol>
</template>

<style lang="scss" scoped>
.build-base {
  height: 36px;
  background: #777;
  color: white;
  line-height: 36px;
  vertical-align: middle;
  border: solid #555 1px;
}
</style>
