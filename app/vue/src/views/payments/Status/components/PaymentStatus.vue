<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { useProCash } from '@/store/pinia/proCash'
import { numFormat, dateFormat } from '@/utils/baseMixins'
import { TableSecondary } from '@/utils/cssMixins'

defineProps({
  date: { type: String, default: '' },
  orderGroup: { type: Array, default: () => [] },
  unitType: { type: Array, default: () => [] },
})
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="7">
          <strong>
            <CIcon name="cilFolderOpen" />
            분양대금 납부현황 등
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
        <CTableHeaderCell>수량</CTableHeaderCell>
        <CTableHeaderCell>단가(평균)</CTableHeaderCell>
        <CTableHeaderCell>실수납 금액</CTableHeaderCell>
        <CTableHeaderCell>미수 금액</CTableHeaderCell>
        <CTableHeaderCell>합계</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <template v-for="(order, oi) in orderGroup" :key="oi">
        <CTableRow v-for="(type, ti) in unitType" :key="ti" class="text-right">
          <CTableHeaderCell
            v-if="oi === 0 && ti === 0"
            class="text-center"
            :rowspan="orderGroup.length * unitType.length"
          >
            계약
          </CTableHeaderCell>
          <CTableHeaderCell
            v-if="ti === 0"
            class="text-center"
            :rowspan="unitType.length"
          >
            {{ order.order_group_name }}
          </CTableHeaderCell>
          <CTableHeaderCell class="text-left" :color="TableSecondary">
            <v-icon icon="mdi mdi-square" :color="type.color" size="sm" />
            {{ type.name }}
          </CTableHeaderCell>
          <CTableDataCell>87</CTableDataCell>
          <CTableDataCell>339,000,000</CTableDataCell>
          <CTableDataCell>6,840,060,000</CTableDataCell>
          <CTableDataCell>22,664,511,000</CTableDataCell>
          <CTableDataCell>29,504,571,000</CTableDataCell>
        </CTableRow>
      </template>

      <template v-for="(order, oi) in orderGroup" :key="oi">
        <CTableRow v-for="(type, ti) in unitType" :key="ti" class="text-right">
          <CTableHeaderCell
            v-if="oi === 0 && ti === 0"
            class="text-center"
            :rowspan="orderGroup.length * unitType.length"
          >
            미계약
          </CTableHeaderCell>
          <CTableHeaderCell
            v-if="ti === 0"
            class="text-center"
            :rowspan="unitType.length"
          >
            {{ order.order_group_name }}
          </CTableHeaderCell>
          <CTableHeaderCell class="text-left" :color="TableSecondary">
            <v-icon icon="mdi mdi-square" :color="type.color" size="sm" />
            {{ type.name }}
          </CTableHeaderCell>
          <CTableDataCell>-</CTableDataCell>
          <CTableDataCell>-</CTableDataCell>
          <CTableDataCell>-</CTableDataCell>
          <CTableDataCell>-</CTableDataCell>
          <CTableDataCell>-</CTableDataCell>
        </CTableRow>
      </template>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right">
        <CTableHeaderCell colspan="3" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>
