<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { useProCash } from '@/store/pinia/proCash'
import { numFormat, dateFormat } from '@/utils/baseMixins'
import { TableSecondary } from '@/utils/cssMixins'

defineProps({ date: { type: String, default: '' } })
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
        <CTableHeaderCell>단가</CTableHeaderCell>
        <CTableHeaderCell>실수납금액</CTableHeaderCell>
        <CTableHeaderCell>미수금액</CTableHeaderCell>
        <CTableHeaderCell>합계</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center" rowspan="12">
          계약
        </CTableHeaderCell>
        <CTableHeaderCell class="text-center" rowspan="3">
          1차조합원
        </CTableHeaderCell>
        <CTableHeaderCell class="text-center">72</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center">84A</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center">84B</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center" rowspan="3">
          2차조합원
        </CTableHeaderCell>
        <CTableHeaderCell class="text-center">72</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center">84A</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center">84B</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center" rowspan="3">
          3차조합원
        </CTableHeaderCell>
        <CTableHeaderCell class="text-center">72</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center">84A</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center">84B</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>

      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center" rowspan="3">
          일반분양
        </CTableHeaderCell>
        <CTableHeaderCell class="text-center">72</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center">84A</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-right">
        <CTableHeaderCell class="text-center">84B</CTableHeaderCell>
        <CTableDataCell>87</CTableDataCell>
        <CTableDataCell>339,000</CTableDataCell>
        <CTableDataCell>6,840,060</CTableDataCell>
        <CTableDataCell>22,664,511</CTableDataCell>
        <CTableDataCell>29,504,571</CTableDataCell>
      </CTableRow>
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
