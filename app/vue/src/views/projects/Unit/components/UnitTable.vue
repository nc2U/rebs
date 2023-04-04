<script lang="ts" setup>
import { computed } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import { HouseUnit } from '@/store/types/project'
import Unit from '@/views/projects/Unit/components/Unit.vue'
import UnitForm from './UnitForm.vue'

defineProps({ bldgName: { type: String, default: '' } })
const emit = defineEmits(['on-update', 'on-delete'])

const maxFloor = computed(() =>
  Math.max(...simpleUnits.value.map((u: { floor: number }) => u.floor)),
)

const proDataStore = useProjectData()
const simpleUnits = computed(() => proDataStore.simpleUnits)
const lineList = computed(() =>
  [...new Set(simpleUnits.value.map((u: { line: number }) => u.line))].sort(),
)
const houseUnitList = computed(() => proDataStore.houseUnitList)

const lineClass = computed(() =>
  lineList.value.length > 8 ? 'col-xl-12' : 'col-xl-6',
)
const listsClass = computed(() =>
  lineList.value.length > 8 ? 'col-xl-12' : 'col-xl-6',
)

const getUnit = (line: number, floor: number) =>
  simpleUnits.value
    .filter((u: { line: number }) => u.line === line)
    .filter((u: { floor: number }) => u.floor === floor)[0]

const onUpdate = (payload: HouseUnit) => emit('on-update', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CContainer>
    <CRow v-if="simpleUnits.length === 0">
      <CCol class="text-center p-5 text-danger">
        등록된 데이터가 없습니다.
      </CCol>
    </CRow>

    <CRow v-else>
      <CCol class="p-5" :class="lineClass">
        <CRow v-for="i in maxFloor" :key="i">
          <Unit
            v-for="line in lineList"
            :key="`${line}-${i}`"
            :unit="getUnit(line, maxFloor + 1 - i)"
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

      <CCol :class="listsClass">
        <CTable hover responsive align="middle">
          <colgroup>
            <col width="12%" />
            <!--            <col width="15%" />-->
            <col width="12%" />
            <!--            <col width="9%" />-->
            <!--            <col width="10%" />-->
            <col width="8%" />
            <col width="20%" />
            <col width="14%" />
          </colgroup>
          <CTableHead>
            <CTableRow class="text-center">
              <CTableHeaderCell>타입</CTableHeaderCell>
              <!--              <CTableHeaderCell>층범위타입</CTableHeaderCell>-->
              <CTableHeaderCell>호수</CTableHeaderCell>
              <!--              <CTableHeaderCell>라인</CTableHeaderCell>-->
              <!--              <CTableHeaderCell>층수</CTableHeaderCell>-->
              <CTableHeaderCell>홀딩여부</CTableHeaderCell>
              <CTableHeaderCell>홀딩사유</CTableHeaderCell>
              <CTableHeaderCell>비고</CTableHeaderCell>
            </CTableRow>
          </CTableHead>

          <CTableBody>
            <UnitForm
              v-for="unit in houseUnitList"
              :key="unit.pk"
              :unit="unit"
              @on-update="onUpdate"
              @on-delete="onDelete"
            />
          </CTableBody>
        </CTable>
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
