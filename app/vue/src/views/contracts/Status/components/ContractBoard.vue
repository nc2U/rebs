<script lang="ts" setup>
import { computed } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import Building from '@/views/contracts/Status/components/Building.vue'

import { KeyUnit } from '@/store/types/project'

type UnitType = {
  bldg: number
  is_hold: boolean
  color: string
  line: number
  name: string
  key_unit: KeyUnit
  floor: number
}

const projectDataStore = useProjectData()

const simpleUnits = computed(() => projectDataStore.simpleUnits)

const getBldg = computed(() =>
  [...new Set(simpleUnits.value.map((u: UnitType) => u.bldg))].sort(),
)
const maxFloor = computed(() =>
  Math.max(...simpleUnits.value.map((u: UnitType) => u.floor)),
)

const getUnits = (bldg: number): UnitType[] =>
  simpleUnits.value.filter((u: UnitType) => u.bldg === bldg)
</script>

<template>
  <CContainer>
    <div
      v-if="simpleUnits.length === 0"
      class="row justify-content-center pt-5 m-5"
    >
      <CSpinner color="grey" />
    </div>

    <CRow v-else>
      <Building
        v-for="bldg in getBldg"
        :key="bldg"
        :bldg="bldg"
        :max-floor="maxFloor"
        :units="getUnits(bldg)"
      />
    </CRow>
  </CContainer>
</template>
