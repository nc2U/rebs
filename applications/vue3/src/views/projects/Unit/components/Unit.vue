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

<script lang="ts">
import { defineComponent } from 'vue'
import floor from '@/views/projects/Floor/components/Floor.vue'

export default defineComponent({
  name: 'Unit',
  components: {},
  props: ['units', 'floor', 'line'],
  setup() {
    return {}
  },
  computed: {
    unit() {
      return this.units
        .filter((u: any) => u.line == this.line)
        .filter((u: any) => u.floor == this.floor)[0]
    },
    isBuild() {
      return this.unit || this.floor < 3
    },
    color() {
      return this.unit ? this.unit.color : '#999'
    },
  },
})
</script>

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
