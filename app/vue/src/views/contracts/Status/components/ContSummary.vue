<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { numFormat } from '@/utils/baseMixins'
import {
  headerSecondary,
  headerSuccess,
  headerPrimary,
} from '@/utils/cssMixins'

const store = useStore()

// const houseUnitNum = computed(() => store.state.project.houseUnitNum)
const simpleTypes = computed(() => store.getters['project/simpleTypes'])
const unitSummary = computed(() => store.getters['project/unitSummary'])
</script>

<template>
  <CRow>
    <CCol lg="6">
      <CTable hover responsive bordered align="middle">
        <colgroup>
          <col width="25%" />
          <col width="25%" />
          <col width="25%" />
          <col width="25%" />
        </colgroup>
        <CTableBody>
          <CTableRow>
            <CTableHeaderCell :color="headerSecondary">
              총세대수
            </CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.totalNum) }}
            </CTableDataCell>
            <CTableHeaderCell :color="headerSecondary">
              홀딩세대
            </CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.holdNum) }}
            </CTableDataCell>
          </CTableRow>

          <CTableRow>
            <CTableHeaderCell :color="headerSuccess">청약세대</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.appNum) }}
            </CTableDataCell>
            <CTableHeaderCell :color="headerPrimary">계약세대</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.contNum) }}
            </CTableDataCell>
          </CTableRow>

          <CTableRow>
            <CTableHeaderCell :color="headerSecondary">합계</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.appNum + unitSummary.contNum) }}
            </CTableDataCell>
            <CTableHeaderCell :color="headerSecondary">
              잔여세대
            </CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{
                numFormat(
                  unitSummary.totalNum -
                    unitSummary.appNum -
                    unitSummary.contNum,
                )
              }}
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
    <CCol lg="6">
      <span v-for="type in simpleTypes" :key="type.pk" class="mr-3">
        <div class="cube mr-1" :style="`background-color: ${type.color};`" />
        {{ type.name }}
      </span>
    </CCol>
  </CRow>
</template>

<style lang="scss" scoped>
.cube {
  width: 12px;
  height: 12px;
  display: inline-block;
}
</style>
