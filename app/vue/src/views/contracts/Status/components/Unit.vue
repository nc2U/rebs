<script lang="ts" setup>
import { computed } from 'vue'

const props = defineProps({
  units: { type: Object, default: null },
  unit: { type: Object, default: null },
  floor: { type: Number, default: 1 },
  line: { type: Number, default: 1 },
  maxPiloti: { type: Number, default: 1 },
  firstLine: { type: Number, default: 1 },
})

const isPiloti = computed(() => !props.unit && props.floor < props.maxPiloti)
const isContract = computed(() => !!props.unit.key_unit?.contract)
const contractor = computed(() =>
  isContract.value ? props.unit.key_unit.contract.contractor.name : '',
)
const contractorPk = computed(() =>
  isContract.value ? props.unit.key_unit.contract.contractor.pk : '',
)
const status = computed(() =>
  isContract.value ? props.unit.key_unit.contract.contractor.status : '',
)
const isHold = computed(() => (isContract.value ? props.unit.is_hold : ''))
const statusColor = computed(() => {
  let color = ''
  if (props.unit) {
    color = '#FFF'
    if (isContract.value) {
      if (status.value === '1') color = '#FFFF99'
      if (status.value === '2') color = '#DDD'
      if (isHold.value) color = '#999'
    }
  }
  return color
})
</script>

<template>
  <div class="unit">
    <div
      class="unit-name"
      :class="{
        firstClass: (isPiloti || unit) && line === firstLine,
        restClass: (isPiloti || unit) && line !== firstLine,
        piloti: isPiloti,
      }"
      :style="`background-color: ${unit ? unit.color : ''}`"
    >
      <span v-if="unit" style="color: #666">{{ unit.name }}</span>
    </div>

    <div
      class="status"
      :class="{
        firstClass: unit && line === firstLine,
        restClass: unit && line !== firstLine,
        firstPiloti: isPiloti && line === 1,
        restPiloti: isPiloti && line !== 1,
        piloti: isPiloti,
      }"
      :style="`background-color: ${statusColor};`"
    >
      <span v-if="unit && unit.key_unit && unit.key_unit.contract">
        <router-link
          :to="{
            name: '계약 등록 수정',
            query: { contractor: contractorPk },
          }"
        >
          {{ contractor }}
        </router-link>
      </span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.unit {
  width: 40px;
  height: 40px;
  padding: 0;
  font-size: 10px;
  text-align: center;
  vertical-align: middle;
}

.unit-name {
  height: 20px;
  line-height: 20px;
  padding: 0;
}

.status {
  height: 20px;
  line-height: 20px;
  padding: 0;
}

.firstClass {
  border-width: 1px 1px 0 1px;
  border-style: solid;
  border-color: #999;
}

.firstPiloti {
  border-width: 0 1px 0 1px;
  border-style: solid;
  border-color: #999;
}

.restClass {
  border-width: 1px 1px 0 0;
  border-style: solid;
  border-color: #999;
}

.restPiloti {
  border-width: 0 1px 0 0;
  border-style: solid;
  border-color: #999;
}

.piloti {
  background-color: #bbb;
  border-color: #999;
}
</style>
