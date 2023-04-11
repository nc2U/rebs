<script lang="ts" setup>
import { ref, computed } from 'vue'

const props = defineProps({
  units: { type: Object, default: null },
  floor: { type: Number, default: 1 },
  line: { type: Number, default: 1 },
  lineList: { type: Array, default: () => [] },
})

const maxPiloti = ref(3) // 맥스 피로티 층

const unit = computed(
  () =>
    props.units
      .filter((u: { line: number }) => u.line == props.line)
      .filter((u: { floor: number }) => u.floor == props.floor)[0],
)
const isPiloti = computed(() => !unit.value && props.floor < maxPiloti.value)
const isFirst = computed(() =>
  props.floor > maxPiloti.value
    ? props.units
        .filter((u: { floor: number }) => u.floor == props.floor)
        .map((u: { line: number }) => u.line)
        .sort()[0]
    : 1,
)
const isContract = computed(() => !!unit.value.key_unit?.contract)
const contractor = computed(() =>
  isContract.value ? unit.value.key_unit.contract.contractor.name : '',
)
const status = computed(() =>
  isContract.value ? unit.value.key_unit.contract.contractor.status : '',
)
const isHold = computed(() => (isContract.value ? unit.value.is_hold : ''))
const statusColor = computed(() => {
  let color = ''
  if (unit.value) {
    color = '#FFF'
    if (isContract.value) {
      if (status.value === '1') color = '#D5F1DE'
      if (status.value === '2') color = '#CBC7EC'
      if (isHold.value) color = '#555'
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
        firstline: (isPiloti || unit) && line === isFirst,
        restline: (isPiloti || unit) && line !== isFirst,
        piloti: isPiloti,
      }"
      :style="`background-color: ${unit ? unit.color : ''}`"
    >
      <span v-if="unit" style="color: #666">{{ unit.name }}</span>
    </div>

    <div
      class="status"
      :class="{
        firstline: unit && line === isFirst,
        restline: unit && line !== isFirst,
        firstPiloti: isPiloti && line === 1,
        restPiloti: isPiloti && line !== 1,
        piloti: isPiloti,
      }"
      :style="`background-color: ${statusColor};`"
    >
      <span v-if="unit && unit.key_unit && unit.key_unit.contract">
        <router-link
          :to="{
            name: '계약 등록 관리',
            query: { contract: unit.key_unit.contract.pk },
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

.firstline {
  border-width: 1px 1px 0 1px;
  border-style: solid;
  border-color: #999;
}

.firstPiloti {
  border-width: 0 1px 0 1px;
  border-style: solid;
  border-color: #999;
}

.restline {
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
  background-color: #ccc;
  border-color: #999;
}
</style>
