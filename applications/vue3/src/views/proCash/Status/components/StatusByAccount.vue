<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="10%" />
      <col width="30%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="5">
          <strong>
            <CIcon name="cilFolderOpen" />
            프로젝트 계좌별 자금현황
          </strong>
          <small>(2022-03-20) 현재</small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="dark" class="text-center">
        <CTableHeaderCell colspan="2">구분</CTableHeaderCell>
        <CTableHeaderCell>전일잔고</CTableHeaderCell>
        <CTableHeaderCell>금일입금(증가)</CTableHeaderCell>
        <CTableHeaderCell>금일출금(감소)</CTableHeaderCell>
        <CTableHeaderCell>금일잔고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow class="text-right" v-for="i in 20" :key="i">
        <CTableDataCell class="text-center" rowspan="20" v-if="i === 1">
          보통예금
        </CTableDataCell>
        <CTableDataCell class="text-left">아시아-신청금(외환)</CTableDataCell>
        <CTableDataCell>37,893,237</CTableDataCell>
        <CTableDataCell>-</CTableDataCell>
        <CTableDataCell>-</CTableDataCell>
        <CTableDataCell>37,893,237</CTableDataCell>
      </CTableRow>

      <CTableRow color="dark" class="text-right">
        <CTableHeaderCell colspan="2" class="text-center">
          현금성 자산 계
        </CTableHeaderCell>
        <CTableHeaderCell>9,282,316,408</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>9,282,316,408</CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'StatusByAccount',
  components: {},
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
