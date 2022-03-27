<template>
  <CCol class="ml-4 mt-5">
    <CRow v-for="i in maxFloor" :key="i">
      <Unit
        v-for="line in lineList"
        :key="line"
        :units="units"
        :floor="maxFloor + 1 - i"
        :line="line"
      />
    </CRow>
    <CRow v-if="lineList">
      <div
        class="text-center build-base"
        :style="{
          width: `${40 * lineList.length}px`,
        }"
      >
        {{ bldg }}동
      </div>
    </CRow>
  </CCol>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Unit from '@/views/contracts/Status/components/Unit.vue'

export default defineComponent({
  name: 'Building',
  components: { Unit },
  props: { bldg: Number, maxFloor: Number, units: Object },
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {
    lineList(this: any) {
      return [...new Set(this.units.map((u: any) => u.line))].sort()
    },
  },
  methods: {},
})
</script>

<style lang="scss" scoped>
.build-base {
  height: 36px;
  background: #777;
  color: white;
  line-height: 36px;
  vertical-align: middle;
}
</style>
