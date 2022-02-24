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
        <CTableHeaderCell>{{ numFormat(total_budget) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(2000) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(2000) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(2000) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(2000) }}</CTableHeaderCell>
      </CTableRow>

      <CTableRow class="text-right" v-for="type in unitTypeList" :key="type.pk">
        <CTableHeaderCell class="text-left pl-5">
          <CIcon
            name="cib-node-js"
            :style="{ color: type.color }"
            size="sm"
            class="mr-1"
          />
          {{ type.name }}
        </CTableHeaderCell>
        <CTableDataCell>
          {{ numFormat(type.average_price * type.num_unit) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ numFormat(sellAmount(type.pk, type.average_price)) }}
        </CTableDataCell>
        <CTableDataCell class="text-primary">
          {{ numFormat(paymentByType(type.pk)) }}
        </CTableDataCell>
        <CTableDataCell class="text-danger">
          {{
            numFormat(
              sellAmount(type.pk, type.average_price) - paymentByType(type.pk),
            )
          }}
        </CTableDataCell>
        <CTableDataCell>
          {{
            numFormat(
              type.average_price * type.num_unit -
                sellAmount(type.pk, type.average_price),
            )
          }}
        </CTableDataCell>
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
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractSummary',
  mixins: [commonMixin],
  props: {
    project: {
      type: Object,
    },
  },
  computed: {
    total_budget() {
      return this.unitTypeList
        .map((t: any) => t.average_price * t.num_unit)
        .reduce((x: number, y: number) => x + y)
    },
    ...mapState('project', ['unitTypeList']),
    ...mapState('payment', ['paySumList', 'contNumList']),
    ...mapGetters('contract', ['getSubs', 'getConts']),
  },
  methods: {
    sellAmount(type: number, price = 0) {
      const cont_num = this.contNumList
        ? this.contNumList.filter((c: any) => c.unit_type === type)[0].num_cont
        : 0
      return cont_num * price
    },
    paymentByType(type: number) {
      return this.paySumList
        ? this.paySumList.filter((p: any) => p.unit_type === type)[0].type_total
        : 0
    },
  },
})
</script>
