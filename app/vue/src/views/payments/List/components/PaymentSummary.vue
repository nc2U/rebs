<script lang="ts" setup>
import { computed } from 'vue'
import { usePayment } from '@/store/pinia/payment'
import { useProjectData } from '@/store/pinia/project_data'
import { UnitType } from '@/store/types/project'
import { numFormat } from '@/utils/baseMixins'
import { headerSecondary } from '@/utils/cssMixins'

defineProps({ project: { type: Object, default: null } })

const projectDataStore = useProjectData()
const unitTypeList = computed(() => projectDataStore.unitTypeList)

const paymentStore = usePayment()
const paySumList = computed(() => paymentStore.paySumList)
const contNumList = computed(() => paymentStore.contNumList)

const total_budget = computed(() => {
  return unitTypeList.value.length !== 0
    ? unitTypeList.value
        .map((t: UnitType) => t.average_price * t.num_unit)
        .reduce((x: number, y: number) => x + y)
    : 0
})
const totalAmount = computed(() => {
  const types = unitTypeList.value.map((t: UnitType) => t.average_price)
  const nums = contNumList.value.map((c: { num_cont: number }) => c.num_cont)

  let total = 0
  for (let i in types) {
    const type = types[i]
    if (typeof type === 'number' && typeof nums[i] === 'number')
      total += type * nums[i]
  }
  return total
})
const totalPayment = computed(() => {
  return paySumList.value.length !== 0
    ? paySumList.value
        .map((p: { type_total: number }) => p.type_total)
        .reduce((x: number, y: number) => x + y, 0)
    : 0
})

const sellAmount = (type: number, price = 0) => {
  const nums = contNumList.value
    .filter((c: { unit_type: number }) => c.unit_type === type)
    .map((c: { num_cont: number }) => c.num_cont)
  const num = typeof nums[0] === 'number' ? nums[0] : 0
  return num * price
}

const payByType = (type: number) => {
  return paySumList.value
    .filter((p: { unit_type: number }) => p.unit_type === type)
    .map((p: { type_total: number }) => p.type_total)[0]
}
</script>

<template>
  <CTable hover responsive bordered class="mt-3">
    <CTableHead class="text-center" :color="headerSecondary">
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
      <CTableRow v-if="project" class="text-right" color="light">
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

      <CTableRow v-for="type in unitTypeList" :key="type.pk" class="text-right">
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
