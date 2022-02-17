<template>
  <CContainer>
    <CRow v-if="simpleUnits.length === 0">
      <CCol class="text-center p-5 text-danger">
        등록된 데이터가 없습니다.
      </CCol>
    </CRow>

    <CRow v-else>
      <CCol class="p-5">
        <CRow v-for="i in maxFloor" :key="i">
          <Unit
            v-for="line in lineList"
            :key="line"
            :units="simpleUnits"
            :floor="maxFloor + 1 - i"
            :line="line"
          />
        </CRow>
        <CRow v-if="lineList">
          <div
            class="text-center build-base"
            :style="{
              width: `${60 * lineList.length}px`,
            }"
          >
            {{ bldgName }}동
          </div>
        </CRow>
      </CCol>
    </CRow>
  </CContainer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Unit from '@/views/projects/Unit/components/Unit.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'UnitListTable',
  components: { Unit },
  props: ['bldgName'],
  computed: {
    maxFloor(this: any) {
      return Math.max(...this.simpleUnits.map((u: any) => u.floor))
    },
    lineList(this: any) {
      return [...new Set(this.simpleUnits.map((u: any) => u.line))].sort()
    },
    ...mapGetters('project', ['simpleUnits']),
  },
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
