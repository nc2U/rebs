<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import Unit from '@/views/projects/Unit/components/Unit.vue'

defineProps({ bldgName: { type: String, default: '' } })

const store = useStore()

const maxFloor = computed(() =>
  Math.max(...simpleUnits.value.map((u: any) => u.floor)),
)
const simpleUnits = computed(() => store.getters['project/simpleUnits'])
const lineList = computed(() =>
  [...new Set(simpleUnits.value.map((u: any) => u.line))].sort(),
)
</script>

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

<style lang="scss" scoped>
.build-base {
  height: 36px;
  background: #777;
  color: white;
  line-height: 36px;
  vertical-align: middle;
}
</style>
