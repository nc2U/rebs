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

    <CTableBody>
      <CTableRow class="text-right" color="light" v-if="project">
        <CTableHeaderCell class="text-center">
          {{ project.name }}
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(total_budget) }}</CTableHeaderCell>
        <CTableHeaderCell>
          {{ numFormat(totalAmount) }}
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(totalPayment) }}</CTableHeaderCell>
        <CTableHeaderCell>
          {{ numFormat(totalAmount - totalPayment) }}
        </CTableHeaderCell>
        <CTableHeaderCell>
          {{ numFormat(total_budget - totalAmount) }}
        </CTableHeaderCell>
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
          {{ numFormat(payByType(type.pk)) }}
        </CTableDataCell>
        <CTableDataCell class="text-danger">
          {{
            numFormat(
              sellAmount(type.pk, type.average_price) - payByType(type.pk),
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
      return this.unitTypeList.length !== 0
        ? this.unitTypeList
            .map((t: any) => t.average_price * t.num_unit)
            .reduce((x: number, y: number) => x + y)
        : 0
    },
    totalAmount() {
      const types = this.unitTypeList.map((t: any) => t.average_price)
      const nums = this.contNumList.map((c: any) => c.num_cont)

      let total = 0
      for (let i in types) {
        const type = types[i]
        if (typeof type === 'number' && typeof nums[i] === 'number')
          total += type * nums[i]
      }
      return total
    },
    totalPayment() {
      return this.paySumList.length !== 0
        ? this.paySumList
            .map((p: any) => p.type_total)
            .reduce((x: number, y: number) => x + y)
        : 0
    },
    ...mapState('project', ['unitTypeList']),
    ...mapState('payment', ['paySumList', 'contNumList']),
    ...mapGetters('contract', ['getSubs', 'getConts']),
  },
  methods: {
    sellAmount(type: number, price = 0) {
      const nums = this.contNumList
        .filter((c: any) => c.unit_type === type)
        .map((c: any) => c.num_cont)
      const num = typeof nums[0] === 'number' ? nums[0] : 0
      return num * price
    },
    payByType(type: number) {
      return this.paySumList
        .filter((p: any) => p.unit_type === type)
        .map((p: any) => p.type_total)[0]
    },
  },
})
</script>
