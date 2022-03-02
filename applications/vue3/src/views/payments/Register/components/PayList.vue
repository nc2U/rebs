<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="16%"/>
      <col width="18%"/>
      <col width="16%"/>
      <col width="22%"/>
      <col width="18%"/>
      <col width="10%"/>
    </colgroup>

    <CTableHead color="dark">
      <CTableRow class="text-center">
        <CTableHeaderCell>수납일자</CTableHeaderCell>
        <CTableHeaderCell>납부회차</CTableHeaderCell>
        <CTableHeaderCell>수납금액</CTableHeaderCell>
        <CTableHeaderCell>수납계좌</CTableHeaderCell>
        <CTableHeaderCell>입금자명</CTableHeaderCell>
        <CTableHeaderCell>비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody v-if="contract">
      <CTableRow class="text-center" v-for="i in 3" :key="i">
        <CTableDataCell>2022-03-02</CTableDataCell>
        <CTableDataCell>[계약금] - 1차계약금</CTableDataCell>
        <CTableDataCell class="text-right">25,000,000</CTableDataCell>
        <CTableDataCell>국제신탁-분담금(국민)</CTableDataCell>
        <CTableDataCell>김광수902동140</CTableDataCell>
        <CTableDataCell>
          <CButton type="button" color="info" size="sm">보기</CButton>
        </CTableDataCell>
      </CTableRow>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right">
        <CTableHeaderCell color="dark" class="text-center"
        >합계
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell>150,000,000</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>

<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: 'PayList',
  components: {},
  props: {contract: Object},
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
