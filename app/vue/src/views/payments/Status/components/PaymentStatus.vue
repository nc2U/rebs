<script lang="ts" setup>
import { computed } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { TableSecondary } from '@/utils/cssMixins'
import { numFormat, dateFormat } from '@/utils/baseMixins'

defineProps({
  date: { type: String, default: '' },
  sort: { type: String, default: '2' },
})

const proStore = useProject()
const budgetList = computed(() => proStore.proIncBudgetList)

const contStore = useContract()
const orderGroup = computed(() => contStore.orderGroupList)
const contSum = computed(() => contStore.contSummaryList)

const prDataStore = useProjectData()
const unitType = computed(() => prDataStore.unitTypeList)

const getOGName = (og: number) =>
  orderGroup.value.filter(o => o.pk === og)[0].order_group_name

const getUTName = (ut: number) => unitType.value.filter(u => u.pk === ut)[0]

const getContNum = (og: number, ut: number) =>
  contSum.value
    .filter(c => c.order_group === og && c.unit_type === ut)
    .map(c => c.num_cont)[0]

const getUTbyOGNum = (og: number) =>
  budgetList.value.filter(b => b.order_group === og).length

const getFirstType = (og: number) =>
  budgetList.value.filter(b => b.order_group === og)[0].unit_type
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="8%" />
      <col width="8%" />
      <col width="10%" />
      <col width="7%" />
      <col width="7%" />
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="9">
          <strong>
            <CIcon name="cilFolderOpen" />
            차수 및 타입별 수납 현황
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 현재
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>

      <CTableRow :color="TableSecondary" class="text-center" align="middle">
        <CTableHeaderCell rowspan="2">차수</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">타입</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">단가(평균)</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">계획 세대수</CTableHeaderCell>
        <CTableHeaderCell colspan="4">계약 현황</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">미계약 금액</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">합계</CTableHeaderCell>
      </CTableRow>

      <CTableRow :color="TableSecondary" class="text-center">
        <CTableHeaderCell>계약 세대수</CTableHeaderCell>
        <CTableHeaderCell>계약 금액</CTableHeaderCell>
        <CTableHeaderCell>실수납 금액</CTableHeaderCell>
        <CTableHeaderCell>미수 금액</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow v-for="bg in budgetList" :key="bg.pk" class="text-right">
        <CTableDataCell
          v-if="bg.unit_type === getFirstType(bg.order_group)"
          :rowspan="getUTbyOGNum(bg.order_group)"
          class="text-center"
        >
          {{ getOGName(bg.order_group) }}
        </CTableDataCell>
        <CTableDataCell class="text-left pl-4">
          <v-icon
            icon="mdi mdi-square"
            :color="getUTName(bg.unit_type).color"
            size="sm"
          />
          {{ getUTName(bg.unit_type).name }}
        </CTableDataCell>
        <CTableDataCell>{{ numFormat(bg.average_price) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(bg.quantity) }}</CTableDataCell>
        <CTableDataCell>
          {{ numFormat(getContNum(bg.order_group, bg.unit_type)) }}
        </CTableDataCell>
        <CTableDataCell>
          {{
            numFormat(
              bg.average_price * getContNum(bg.order_group, bg.unit_type),
            )
          }}
        </CTableDataCell>
        <CTableDataCell>{{ numFormat(1 + 1) }}</CTableDataCell>
        <CTableDataCell>
          {{
            numFormat(
              bg.average_price * getContNum(bg.order_group, bg.unit_type) -
                (1 + 1),
            )
          }}
        </CTableDataCell>
        <CTableDataCell>
          {{
            numFormat(
              bg.average_price *
                (bg.quantity - (getContNum(bg.order_group, bg.unit_type) || 0)),
            )
          }}
        </CTableDataCell>
        <CTableDataCell>{{ numFormat(bg.budget) }}</CTableDataCell>
      </CTableRow>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right" :color="TableSecondary">
        <CTableHeaderCell colspan="2" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(625) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(625) }}</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(44000000000) }}</CTableHeaderCell>
        <CTableHeaderCell>
          {{ numFormat(330000000000 - 44000000000) }}
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(330000000000) }}</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>
