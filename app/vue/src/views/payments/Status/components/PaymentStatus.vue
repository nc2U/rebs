<script lang="ts" setup>
import { computed } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { TableSecondary } from '@/utils/cssMixins'
import { numFormat, dateFormat } from '@/utils/baseMixins'

const props = defineProps({
  date: { type: String, default: '' },
  sort: { type: String, default: '2' },
})

const proStore = useProject()
const budgetList = computed(() => proStore.proIncBudgetList)

const prDataStore = useProjectData()
const unitType = computed(() => prDataStore.unitTypeList)

const contStore = useContract()
const orderGroup = computed(() => contStore.orderGroupList)
const contSum = computed(() => contStore.contSummaryList)

const getNums = (og: number, ut: number) =>
  contSum.value
    .filter(c => c.order_group === og && c.unit_type === ut)
    .map(c => c.num_cont)[0]

const typeContNum = (type: number) =>
  contSum.value
    ?.filter(c => c.unit_type === type)
    ?.map(c => c.num_cont)
    .reduce((pn, cn) => pn + cn, 0)

const getUnitPrice = (og: number, ut: number) => {
  const unit = budgetList.value.filter(
    b => b.order_group === og && b.unit_type === ut,
  )[0]
  return unit ? unit.average_price : 0
}

const getQuantity = (og: number, ut: number) => {
  const unit = budgetList.value.filter(
    b => b.order_group === og && b.unit_type === ut,
  )[0]
  return unit ? unit.quantity : 0
}
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="6%" />
      <col width="9%" />
      <col width="9%" />
      <col width="8%" />
      <col width="8%" />
      <col width="14%" />
      <col width="15%" />
      <col width="15%" />
      <col width="16%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="8">
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

      <CTableRow :color="TableSecondary" class="text-center">
        <CTableHeaderCell colspan="2">구분</CTableHeaderCell>
        <CTableHeaderCell>타입</CTableHeaderCell>
        <CTableHeaderCell>계획 세대수</CTableHeaderCell>
        <CTableHeaderCell>계약 세대수</CTableHeaderCell>
        <CTableHeaderCell>단가(평균)</CTableHeaderCell>
        <CTableHeaderCell>실수납 금액</CTableHeaderCell>
        <CTableHeaderCell>미수 금액</CTableHeaderCell>
        <CTableHeaderCell>합계</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <template v-if="sort !== '0'">
        <template v-for="(order, oi) in orderGroup" :key="oi">
          <CTableRow
            v-for="(type, ti) in unitType"
            :key="ti"
            class="text-right"
          >
            <CTableHeaderCell
              v-if="oi === 0 && ti === 0"
              class="text-center"
              :color="TableSecondary"
              :rowspan="orderGroup.length * unitType.length"
            >
              계약
            </CTableHeaderCell>
            <CTableDataCell
              v-if="ti === 0"
              class="text-center"
              :color="TableSecondary"
              :rowspan="unitType.length"
            >
              {{ order.order_group_name }}
            </CTableDataCell>
            <CTableDataCell class="text-left pl-4">
              <v-icon icon="mdi mdi-square" :color="type.color" size="sm" />
              {{ type.name }}
            </CTableDataCell>
            <CTableDataCell>
              {{ numFormat(getQuantity(order.pk, type.pk)) }}
            </CTableDataCell>
            <CTableDataCell>
              {{ numFormat(getNums(order.pk, type.pk)) }}
            </CTableDataCell>
            <CTableDataCell>
              {{ numFormat(getUnitPrice(order.pk, type.pk)) }}
            </CTableDataCell>
            <CTableDataCell>{{ numFormat(100) }}</CTableDataCell>
            <CTableDataCell>
              {{
                numFormat(
                  getNums(order.pk, type.pk) * getUnitPrice(order.pk, type.pk) -
                    100 || 0,
                )
              }}
            </CTableDataCell>
            <CTableDataCell>
              {{
                numFormat(
                  getNums(order.pk, type.pk) *
                    getUnitPrice(order.pk, type.pk) || 0,
                )
              }}
            </CTableDataCell>
          </CTableRow>
        </template>
      </template>

      <template v-if="sort !== '1'">
        <CTableRow v-for="(type, ti) in unitType" :key="ti" class="text-right">
          <CTableHeaderCell
            v-if="ti === 0"
            class="text-center"
            :color="TableSecondary"
            :rowspan="unitType.length"
            colspan="2"
          >
            미계약
          </CTableHeaderCell>
          <CTableDataCell class="text-left pl-4">
            <v-icon icon="mdi mdi-square" :color="type.color" size="sm" />
            {{ type.name }}
          </CTableDataCell>
          <CTableDataCell></CTableDataCell>
          <CTableDataCell>
            {{ numFormat(type.num_unit - typeContNum(type.pk)) }}
          </CTableDataCell>
          <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
        </CTableRow>
      </template>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right" :color="TableSecondary">
        <CTableHeaderCell colspan="3" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(625) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(625) }}</CTableHeaderCell>
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
