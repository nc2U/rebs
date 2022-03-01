<template>
  <CTable hover responsive>
    <colgroup>
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
    </colgroup>

    <CTableHead color="dark">
      <CTableRow class="text-center">
        <CTableHeaderCell>수납일자</CTableHeaderCell>
        <CTableHeaderCell>납부회차</CTableHeaderCell>
        <CTableHeaderCell>수납금액</CTableHeaderCell>
        <CTableHeaderCell>수납계좌</CTableHeaderCell>
        <CTableHeaderCell>입금자명</CTableHeaderCell>
        <!--        <CTableHeaderCell>비고</CTableHeaderCell>-->
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow>
        <CTableDataCell>1</CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <!--        <CTableDataCell></CTableDataCell>-->
      </CTableRow>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right">
        <CTableHeaderCell color="dark" class="text-center"
          >합계
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell>50,000,000</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'PayList',
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
