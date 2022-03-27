<template>
  <div
    class="unit"
    :class="{
      firstline: unit && line === 1,
      restline: unit && line !== 1,
      piloti: isPiloti,
    }"
    :style="`background-color: ${unit ? unit.color : ''}`"
  >
    <span v-if="unit">{{ unit.name }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Unit',
  props: { units: Array, floor: Number, line: Number },
  computed: {
    unit(this: any) {
      return this.units
        .filter((u: any) => u.line == this.line)
        .filter((u: any) => u.floor == this.floor)[0]
    },
    isPiloti(this: any) {
      return !this.unit && this.floor < 3
    },
  },
})
</script>

<style lang="scss" scoped>
.unit {
  width: 40px;
  height: 20px;
  line-height: 20px;
  padding: 0;
  font-size: 10px;
  text-align: center;
  vertical-align: middle;
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

.piloti {
  background-color: #999;
}
</style>
