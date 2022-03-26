<template>
  <CRow>
    <CCol lg="6">
      <CTable hover responsive bordered align="middle">
        <colgroup>
          <col width="25%" />
          <col width="25%" />
          <col width="25%" />
          <col width="25%" />
        </colgroup>
        <CTableBody>
          <CTableRow>
            <CTableHeaderCell color="dark">총세대수</CTableHeaderCell>
            <CTableDataCell class="text-right">-</CTableDataCell>
            <CTableHeaderCell color="dark">홀딩세대</CTableHeaderCell>
            <CTableDataCell class="text-right">-</CTableDataCell>
          </CTableRow>

          <CTableRow>
            <CTableHeaderCell color="success">청약세대</CTableHeaderCell>
            <CTableDataCell class="text-right">-</CTableDataCell>
            <CTableHeaderCell color="primary">계약세대</CTableHeaderCell>
            <CTableDataCell class="text-right">-</CTableDataCell>
          </CTableRow>

          <CTableRow>
            <CTableHeaderCell color="dark">합계</CTableHeaderCell>
            <CTableDataCell class="text-right">-</CTableDataCell>
            <CTableHeaderCell color="dark">잔여세대</CTableHeaderCell>
            <CTableDataCell class="text-right">-</CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
    <CCol lg="6">74 84A 84B</CCol>
  </CRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContSummary',
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
