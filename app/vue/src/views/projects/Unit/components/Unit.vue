<script lang="ts" setup>
import { computed, type PropType } from 'vue'
import type { SimpleUnit } from '@/store/types/project'

const props = defineProps({
  unit: { type: Object as PropType<SimpleUnit | null>, default: null },
  floor: { type: Number, default: 1 },
  line: { type: Number, default: 1 },
})

const color = computed(() => {
  if (props.unit?.color) return props.unit.color
  return props.floor < 3 ? '#ccc' : ''
})
</script>

<template>
  <div
    class="unit"
    :class="{
      border: !!unit || floor < 3,
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
</style>
