<template>
  <CTable hover responsive bordered class="mt-3">
    <CTableHead class="text-center" color="dark">
      <CTableRow align="middle">
        <CTableHeaderCell rowspan="2">프로젝트명</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">타입</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">세대수</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">청약건수</CTableHeaderCell>
        <CTableHeaderCell
          :colspan="orderGroupList.length === 1 ? 1 : orderGroupList.length + 1"
        >
          계약건수
        </CTableHeaderCell>
        <CTableHeaderCell rowspan="2">잔여세대</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">계약율</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">분양율(청약+계약)</CTableHeaderCell>
      </CTableRow>

      <CTableRow v-if="orderGroupList.length > 1">
        <CTableHeaderCell v-for="order in orderGroupList" :key="order.pk">
          {{ order.order_group_name }}
        </CTableHeaderCell>

        <CTableHeaderCell v-if="orderGroupList.length > 1">
          합계
        </CTableHeaderCell>
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
        <!--  타입별 세대수 -->
        <CTableDataCell>{{ numFormat(type.num_unit) }}세대</CTableDataCell>
        <!-- 타입별 청약건수-->
        <CTableDataCell>{{ numFormat(0) }}</CTableDataCell>
        <!-- 타입별 계약건수-->
        <CTableDataCell v-for="order in orderGroupList" :key="order.pk">
          {{ numFormat(126) }}
        </CTableDataCell>

        <!-- 차수별 계약건수 합계 -->
        <CTableDataCell v-if="orderGroupList.length > 1">
          {{ numFormat(126) }}
        </CTableDataCell>
        <!--잔여세대-->
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <!-- 계약율-->
        <CTableDataCell>{{ ratioFormat(98.5) }}</CTableDataCell>
        <!-- 분양율(청약+계약)-->
        <CTableDataCell>{{ ratioFormat(98.5) }}</CTableDataCell>
      </CTableRow>

      <CTableRow color="dark" class="text-right">
        <CTableDataCell class="text-center"> 합계</CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <!-- 타입별 세대수 합계-->
        <CTableDataCell>{{ numFormat(126) }}세대</CTableDataCell>
        <!-- 청약 건수 타입별 합계-->
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <!--차수별 계약건수 타입별 합계-->
        <CTableDataCell v-if="orderGroupList.length === 0">-</CTableDataCell>
        <CTableDataCell v-else v-for="order in orderGroupList" :key="order.pk">
          {{ numFormat(136) }}
        </CTableDataCell>
        <!-- 차수별 타입별 계약건수 총계-->
        <CTableDataCell v-if="orderGroupList.length > 1">
          {{ numFormat(526) }}
        </CTableDataCell>
        <!-- 타입별 잔여세대 합계-->
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <!-- 타입별 계약율 합계-->
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
        <!-- 타입별 분양율(청약+계약) 합계-->
        <CTableDataCell>{{ numFormat(126) }}</CTableDataCell>
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
  },
})
</script>
