<template>
  <CTable hover responsive bordered class="mt-3">
    <CTableHead class="text-center" color="dark">
      <CTableRow align="middle">
        <CTableHeaderCell>프로젝트</CTableHeaderCell>
        <CTableHeaderCell>총 매출예산(A)</CTableHeaderCell>
        <CTableHeaderCell>총 분양금액(B)</CTableHeaderCell>
        <CTableHeaderCell>총 수납금액(C)</CTableHeaderCell>
        <CTableHeaderCell>미 수납금액(B-C)</CTableHeaderCell>
        <CTableHeaderCell>미 분양금액(A-B)</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody v-if="project">
      <CTableRow class="text-right" color="light">
        <CTableHeaderCell class="text-center">
          {{ project.name }}
        </CTableHeaderCell>
        <CTableHeaderCell>1</CTableHeaderCell>
        <CTableHeaderCell>1</CTableHeaderCell>
        <CTableHeaderCell>1</CTableHeaderCell>
        <CTableHeaderCell>1</CTableHeaderCell>
        <CTableHeaderCell>1</CTableHeaderCell>
      </CTableRow>

      <CTableRow class="text-right">
        <!-- 타입만큼 반복 -->
        <CTableHeaderCell class="text-center">74</CTableHeaderCell>
        <CTableDataCell>1</CTableDataCell>
        <CTableDataCell>1</CTableDataCell>
        <CTableDataCell>1</CTableDataCell>
        <CTableDataCell>1</CTableDataCell>
        <CTableDataCell>1</CTableDataCell>
      </CTableRow>

      <CTableRow class="text-right" color="light">
        <CTableHeaderCell class="text-center">근린생활시설</CTableHeaderCell>
        <CTableDataCell>1</CTableDataCell>
        <CTableDataCell>1</CTableDataCell>
        <CTableDataCell>1</CTableDataCell>
        <CTableDataCell>1</CTableDataCell>
        <CTableDataCell>1</CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractSummary',
  components: {},

  mixins: [commonMixin],
  props: {
    project: {
      type: Object,
    },
  },
  computed: {
    ...mapState('contract', ['orderGroupList']),
    ...mapState('project', ['unitTypeList']),
    ...mapGetters('contract', ['getSubs', 'getConts']),
  },
})
</script>
