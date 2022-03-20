<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="25%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="5">
          <strong>
            <CIcon name="cilFolderOpen" />
            프로젝트 당일 입금내역
          </strong>
          <small>(2022-03-20) 기준</small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="dark" class="text-center">
        <CTableHeaderCell>항목</CTableHeaderCell>
        <CTableHeaderCell>세부 항목</CTableHeaderCell>
        <CTableHeaderCell>입금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow class="text-center" v-for="i in 2" :key="i">
        <CTableDataCell> 분(부)담금</CTableDataCell>
        <CTableDataCell> 분(부)담금</CTableDataCell>
        <CTableDataCell class="text-right" color="success">
          25,660,000
        </CTableDataCell>
        <CTableDataCell>무궁화-분담금(국민)</CTableDataCell>
        <CTableDataCell class="text-left">서해동902-130</CTableDataCell>
        <CTableDataCell class="text-left">
          서해동(841301-1) 대금납부
        </CTableDataCell>
      </CTableRow>

      <CTableRow color="dark" class="text-right">
        <CTableHeaderCell colspan="2" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>9,282,316,408</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>

  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="25%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="5">
          <strong>
            <CIcon name="cilFolderOpen" />
            프로젝트 당일 출금내역
          </strong>
          <small>(2022-03-20) 기준</small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="dark" class="text-center">
        <CTableHeaderCell>항목</CTableHeaderCell>
        <CTableHeaderCell>세부 항목</CTableHeaderCell>
        <CTableHeaderCell>출금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow class="text-center" v-for="i in 2" :key="i">
        <CTableDataCell> 분(부)담금</CTableDataCell>
        <CTableDataCell> 분(부)담금</CTableDataCell>
        <CTableDataCell class="text-right" color="danger">
          25,660,000
        </CTableDataCell>
        <CTableDataCell>무궁화-분담금(국민)</CTableDataCell>
        <CTableDataCell class="text-left">서해동902-130</CTableDataCell>
        <CTableDataCell class="text-left">
          서해동(841301-1) 대금납부
        </CTableDataCell>
      </CTableRow>

      <CTableRow color="dark" class="text-right">
        <CTableHeaderCell colspan="2" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>9,282,316,408</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'CashListByDate',
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
