<script lang="ts" setup>
import { computed } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import Unit from '@/views/contracts/Status/components/Unit.vue'

const projectDataStore = useProjectData()

const props = defineProps({
  bldg: { type: Number, default: null },
  maxFloor: { type: Number, default: null },
  units: { type: Object, default: null },
})

const lineList = computed(() =>
  [...new Set(props.units.map((u: { line: number }) => u.line))].sort(),
)
const buildingList = computed(() => projectDataStore.buildingList)

const bldgName = (bldg: number) =>
  buildingList.value
    .filter((b: { pk: number; name: string }) => b.pk === bldg)
    .map(b => b.name)[0]
</script>

<template>
  <CCol class="ml-4 mt-5">
    <CRow v-for="i in maxFloor" :key="i">
      <Unit
        v-for="line in lineList"
        :key="line"
        :units="units"
        :floor="maxFloor + 1 - i"
        :line="line"
        :line-list="lineList"
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
