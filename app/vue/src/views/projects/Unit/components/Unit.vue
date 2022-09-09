<script lang="ts" setup>
import { computed } from 'vue'

const props = defineProps({
  unit: { type: Object, default: null },
  floor: { type: Number, default: 1 },
  line: { type: Number, default: 1 },
})

const isBuild = computed(() => props.unit || props.floor < 3)
const color = computed(() => (props.unit ? props.unit.color : '#ccc'))
</script>

<template>
  <div
    v-if="isBuild"
    class="unit"
    :class="{
      first: line === 1,
      rest: line !== 1,
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

.first {
  border-width: 1px 1px 0 1px;
  border-style: solid;
  border-color: #999;
}

.rest {
  border-width: 1px 1px 0 0;
  border-style: solid;
  border-color: #999;
}
</style>
