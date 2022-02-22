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
        <CTableHeaderCell>{{ numFormat(2000) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(2000) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(2000) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(2000) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(2000) }}</CTableHeaderCell>
      </CTableRow>

      <CTableRow class="text-right" v-for="type in simpleTypes" :key="type.pk">
        <CTableHeaderCell class="text-left pl-5">
          <CIcon
            name="cib-node-js"
            :style="{ color: type.color }"
            size="sm"
            class="mr-1"
          />
          {{ type.name }}
        </CTableHeaderCell>
        <CTableDataCell>{{ numFormat(1000) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(1000) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(1000) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(1000) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(1000) }}</CTableDataCell>
      </CTableRow>

      <CTableRow class="text-right" color="light">
        <CTableHeaderCell class="text-left pl-5">근린생활시설</CTableHeaderCell>
        <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ContractSummary',
  mixins: [commonMixin],
  props: {
    project: {
      type: Object,
    },
  },
  computed: {
    ...mapGetters('project', ['simpleTypes']),
    ...mapGetters('contract', ['getSubs', 'getConts']),
  },
})
</script>
