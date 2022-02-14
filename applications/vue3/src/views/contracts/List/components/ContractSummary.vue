<template>
  <CTable hover responsive bordered class="mt-3">
    <CTableHead class="text-center" color="dark">
      <CTableRow align="middle">
        <CTableHeaderCell rowspan="2">프로젝트명</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">타입</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">세대수</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">청약건수</CTableHeaderCell>
        <CTableHeaderCell :colspan="orderGroupList.length + 1">
          계약건수
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2">잔여세대</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">계약율</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">분양율(청약+계약)</CTableHeaderCell>
      </CTableRow>

      <CTableRow>
        <CTableHeaderCell v-for="order in orderGroupList" :key="order.pk">
          {{ order.order_group_name }}
        </CTableHeaderCell>

        <CTableHeaderCell>합계</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow
        class="text-right"
        align="middle"
        v-for="(type, i) in unitTypeList"
        :key="i"
      >
        <CTableHeaderCell
          class="text-center"
          :rowspan="unitTypeList.length"
          v-if="project && i == 0"
        >
          {{ project.name }}
        </CTableHeaderCell>
        <CTableDataCell class="text-left pl-2">
          <CIcon name="cibDiscover" :style="'color:' + type.color" size="sm" />
          {{ type.name }}
        </CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}세대</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
      </CTableRow>
      <CTableRow color="dark" class="text-right">
        <CTableDataCell class="text-center"> 합계</CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}세대</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>

        <CTableDataCell v-for="order in orderGroupList" :key="order.pk">
          {{ numFormat(126) }}
        </CTableDataCell>

        <CTableDataCell>{{ numFormat(526) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ContractSummary',
  components: {},

  mixins: [commonMixin],
  props: ['project'],
  computed: {
    ...mapState('contract', ['orderGroupList']),
    ...mapState('project', ['unitTypeList']),
  },
})
</script>
