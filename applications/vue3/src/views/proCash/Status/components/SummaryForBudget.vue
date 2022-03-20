<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="5%" />
      <col width="5%" />
      <col width="10%" />
      <col width="10%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="8">
          <strong>
            <CIcon name="cilFolderOpen" />
            사업예산 및 집행현황
          </strong>
          <small>(2022-03-20) 기준</small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="dark" class="text-center">
        <CTableHeaderCell colspan="4">구분</CTableHeaderCell>
        <CTableHeaderCell>예산</CTableHeaderCell>
        <CTableHeaderCell>전월 인출금액 누계</CTableHeaderCell>
        <CTableHeaderCell>당월 인출금액</CTableHeaderCell>
        <CTableHeaderCell>인출금액 합계</CTableHeaderCell>
        <CTableHeaderCell>가용 예산합계</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow class="text-right" v-for="i in 20" :key="i">
        <CTableDataCell
          color="info"
          class="text-center"
          rowspan="20"
          v-if="i === 1"
        >
          사업비
        </CTableDataCell>
        <CTableDataCell class="text-center">건축비</CTableDataCell>
        <CTableDataCell class="text-left">간접공사비</CTableDataCell>
        <CTableDataCell class="text-left">각종 인입비</CTableDataCell>
        <CTableDataCell>911,876,000</CTableDataCell>
        <CTableDataCell>-</CTableDataCell>
        <CTableDataCell>-</CTableDataCell>
        <CTableDataCell>-</CTableDataCell>
        <CTableDataCell>-</CTableDataCell>
      </CTableRow>

      <CTableRow color="dark" class="text-right">
        <CTableHeaderCell colspan="4" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>911,876,000</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'SummaryForBudget',
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {},
  methods: {},
})
</script>
