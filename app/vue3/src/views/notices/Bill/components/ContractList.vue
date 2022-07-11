<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
    </colgroup>

    <CTableHead>
      <CTableRow class="text-center">
        <CTableHeaderCell scope="col">전체</CTableHeaderCell>
        <CTableHeaderCell scope="col">일련번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">차수</CTableHeaderCell>
        <CTableHeaderCell scope="col">타입</CTableHeaderCell>
        <CTableHeaderCell scope="col">동호수</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약자</CTableHeaderCell>
        <CTableHeaderCell scope="col">최종납입회차</CTableHeaderCell>
        <CTableHeaderCell scope="col">납입금액합계</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약일자</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Contract
        v-for="contract in contractIndex"
        :contract="contract"
        :key="contract.pk"
      />
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContractorList',
  components: {},
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
      contractIndex: [],
    }
  },
  computed: {},
  methods: {},
})
</script>
