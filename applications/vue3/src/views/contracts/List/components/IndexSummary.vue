<template>
  <CTable hover responsive bordered class="mt-3">
    <CTableHead class="text-center" color="dark">
      <CTableRow align="middle">
        <CTableHeaderCell rowspan="2">프로젝트명</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">타입</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">세대수</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">청약건수</CTableHeaderCell>
        <CTableHeaderCell colspan="5">계약건수</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">잔여세대</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">계약율</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">분양율(청약+계약)</CTableHeaderCell>
      </CTableRow>

      <CTableRow>
        <CTableHeaderCell>1차조합원</CTableHeaderCell>
        <CTableHeaderCell>2차조합원</CTableHeaderCell>
        <CTableHeaderCell>3차조합원</CTableHeaderCell>
        <CTableHeaderCell>일반분양</CTableHeaderCell>

        <CTableHeaderCell>합계</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow align="middle" class="text-center" v-if="project">
        <CTableHeaderCell rowspan="3"> {{ project.name }}</CTableHeaderCell>
        <CTableDataCell>74</CTableDataCell>
        <CTableDataCell>126세대</CTableDataCell>
        <CTableDataCell>126</CTableDataCell>
        <CTableDataCell>126</CTableDataCell>
        <CTableDataCell>126</CTableDataCell>
        <CTableDataCell>126</CTableDataCell>
        <CTableDataCell>126</CTableDataCell>
        <CTableDataCell>126</CTableDataCell>
        <CTableDataCell>126</CTableDataCell>
        <CTableDataCell>126</CTableDataCell>
        <CTableDataCell>126</CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { CTableDataCell } from '@coreui/vue-pro/src/components/table'

export default defineComponent({
  name: '',
  components: { CTableDataCell },
  data() {
    return {
      sample: '',
    }
  },
  props: {
    project: {
      type: Object,
    },
  },
  computed: {},
  methods: {},
})
</script>
