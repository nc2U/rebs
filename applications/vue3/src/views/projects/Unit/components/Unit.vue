<template>
  <CTableDataCell
    v-if="isBuild"
    class="type84"
    :class="{ boarded: isBuild, piloti: isPiloti }"
    :style="{ background: color }"
  >
    <span v-if="unit">{{ unit.name }}</span>
  </CTableDataCell>
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
.type84 {
  width: 150px;
  height: 16px;
  padding: 0;
  font-size: 10px;
  text-align: center;
  vertical-align: middle;
  border: 0;
}

.piloti {
  background-color: #ccc;
}

.boarded {
  border: solid 1px #999;
}
</style>
