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
      <col width="6%" />
      <col width="9%" />
      <col width="9%" />
      <col width="8%" />
      <col width="16%" />
      <col width="17%" />
      <col width="17%" />
      <col width="18%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="7">
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
            :color="TableSecondary"
            :rowspan="orderGroup.length * unitType.length"
          >
            계약
          </CTableHeaderCell>
          <CTableDataCell
            v-if="ti === 0"
            class="text-center"
            :rowspan="unitType.length"
          >
            {{ order.order_group_name }}
          </CTableDataCell>
          <CTableDataCell class="text-left pl-4">
            <v-icon icon="mdi mdi-square" :color="type.color" size="sm" />
            {{ type.name }}
          </CTableDataCell>
          <CTableDataCell>{{ numFormat(87) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(339000000) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(6840060000) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(22664511000) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(29504571000) }}</CTableDataCell>
        </CTableRow>
      </template>

      <template v-for="(order, oi) in orderGroup" :key="oi">
        <CTableRow v-for="(type, ti) in unitType" :key="ti" class="text-right">
          <CTableHeaderCell
            v-if="oi === 0 && ti === 0"
            class="text-center"
            :color="TableSecondary"
            :rowspan="orderGroup.length * unitType.length"
          >
            미계약
          </CTableHeaderCell>
          <CTableDataCell
            v-if="ti === 0"
            class="text-center"
            :rowspan="unitType.length"
          >
            {{ order.order_group_name }}
          </CTableDataCell>
          <CTableDataCell class="text-left pl-4">
            <v-icon icon="mdi mdi-square" :color="type.color" size="sm" />
            {{ type.name }}
          </CTableDataCell>
          <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
        </CTableRow>
      </template>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right">
        <CTableHeaderCell colspan="3" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(0) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(0) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(0) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(0) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(0) }}</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>
