<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Building from '@/views/contracts/Status/components/Building.vue'

import { KeyUnit } from '@/store/modules/project/state'

type UnitType = {
  bldg: number
  is_hold: boolean
  color: string
  line: number
  name: string
  key_unit: KeyUnit
  floor: number
}

const store = useStore()

const simpleUnits = computed(() => store.getters['project/simpleUnits'])

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
    <CRow v-if="simpleUnits.length === 0">
      <CCol class="text-center p-5 text-danger">
        등록된 데이터가 없습니다.
      </CCol>
    </CRow>

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
