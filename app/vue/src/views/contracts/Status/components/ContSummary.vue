<script lang="ts" setup>
import { computed } from 'vue'
import { useProjectData } from '@/store/pinia/project_data'
import { useContract } from '@/store/pinia/contract'
import { numFormat } from '@/utils/baseMixins'
import {
  headerSecondary,
  headerSuccess,
  headerPrimary,
} from '@/utils/cssMixins'
import { SubsSummary } from '@/store/types/contract'

defineProps({ contractsCount: { type: Number, default: 0 } })

const projectDataStore = useProjectData()

const simpleTypes = computed(() => projectDataStore.simpleTypes)
const unitSummary = computed(() => projectDataStore.unitSummary)

const contractStore = useContract()
const subsSummaryList = computed(() => contractStore.subsSummaryList)

const subsNum = () => {
  // 청약 수
  let subs: SubsSummary[] | number[] = subsSummaryList.value
  subs = subs.map((s: SubsSummary) => s.num_cont)
  return subs.reduce((o: number, n: number) => o + n, 0)
}
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
              {{ numFormat(subsNum()) }}
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
              {{
                numFormat(
                  contractsCount -
                    unitSummary.contNum +
                    subsNum() -
                    unitSummary.appNum,
                )
              }}
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
              {{ numFormat(contractsCount + subsNum()) }}
            </CTableDataCell>
            <CTableHeaderCell :color="headerSecondary">
              잔여세대
            </CTableHeaderCell>
            <CTableDataCell class="text-right">
              {{ numFormat(contractsCount - subsNum() - unitSummary.contNum) }}
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
