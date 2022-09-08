<script lang="ts" setup>
import { computed } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import { numFormat } from '@/utils/baseMixins'
import {
  headerSecondary,
  headerSuccess,
  headerPrimary,
} from '@/utils/cssMixins'

defineProps({ contractsCount: { type: Number, default: 0 } })

const projectDataStore = useProjectData()

const simpleTypes = computed(() => projectDataStore.simpleTypes)
const unitSummary = computed(() => projectDataStore.unitSummary)
</script>

<template>
  <CRow>
    <CCol lg="5">
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
            <CTableDataCell class="text-right" colspan="3">
              {{ numFormat(unitSummary.totalNum) }}
            </CTableDataCell>
          </CTableRow>

          <CTableRow>
            <CTableHeaderCell :color="headerSuccess">청약세대</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.appNum) }}
            </CTableDataCell>
            <CTableHeaderCell :color="headerPrimary">계약세대</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(contractsCount) }}
            </CTableDataCell>
          </CTableRow>

          <CTableRow>
            <CTableHeaderCell :color="headerSecondary">
              동호미배정 세대
            </CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(contractsCount - unitSummary.contNum) }}
            </CTableDataCell>
            <CTableHeaderCell :color="headerSecondary">
              홀딩세대
            </CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(unitSummary.holdNum) }}
            </CTableDataCell>
          </CTableRow>

          <CTableRow>
            <CTableHeaderCell :color="headerSecondary">합계</CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(contractsCount) }}
            </CTableDataCell>
            <CTableHeaderCell :color="headerSecondary">
              잔여세대
            </CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{
                numFormat(
                  contractsCount - unitSummary.appNum - unitSummary.contNum,
                )
              }}
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
    <CCol lg="7">
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
