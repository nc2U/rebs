<script lang="ts" setup>
import { computed } from 'vue'

const props = defineProps({
  units: { type: Array, default: [] },
  floor: { type: Number, default: null },
  line: { type: Number, default: null },
})

const unit = computed<any>(
  () =>
    props.units
      .filter((u: any) => u.line == props.line)
      .filter((u: any) => u.floor == props.floor)[0],
)
const isBuild = computed(() => unit.value || props.floor < 3)
const color = computed(() => (unit.value ? unit.value.color : '#999'))
</script>

<template>
  <div
    v-if="isBuild"
    class="unit"
    :class="{
      firstline: line === 1,
      restline: line !== 1,
      piloti: isPiloti,
    }"
    :style="{ background: color }"
  >
    <span v-if="unit">{{ unit.name }}</span>
  </div>
</template>

<style lang="scss" scoped>
.unit {
  width: 60px;
  height: 20px;
  padding: 0;
  font-size: 10px;
  text-align: center;
  vertical-align: middle;
}

.piloti {
  background-color: #ccc;
}

.firstline {
  border-width: 1px 1px 0 1px;
  border-style: solid;
  border-color: #999;
}

.restline {
  border-width: 1px 1px 0 0;
  border-style: solid;
  border-color: #999;
}
</style>
