<template>
  <CTable hover responsive>
    <colgroup>
      <col width="20%"/>
      <col width="20%"/>
      <col width="20%"/>
      <col width="20%"/>
      <col width="20%"/>
    </colgroup>

    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell>납부기일</CTableHeaderCell>
        <CTableHeaderCell>구분</CTableHeaderCell>
        <CTableHeaderCell>약정금액</CTableHeaderCell>
        <CTableHeaderCell>수납금액</CTableHeaderCell>
        <CTableHeaderCell>미(과오)납</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody v-if="contract">
      <CTableRow class="text-right" v-for="i in 11">
        <CTableDataCell class="text-center">2022-03-02</CTableDataCell>
        <CTableDataCell class="text-center">{{ i }}차계약금</CTableDataCell>
        <CTableDataCell>16,800,000</CTableDataCell>
        <CTableDataCell>24,150,000</CTableDataCell>
        <CTableDataCell>-2,650,000</CTableDataCell>
      </CTableRow>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right">
        <CTableHeaderCell color="dark" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell> 385,985,924</CTableHeaderCell>
        <CTableHeaderCell>56,600,000</CTableHeaderCell>
        <CTableHeaderCell>6,200,000</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>

<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: 'PayBoard',
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
