<script lang="ts" setup>
import { computed } from 'vue'
import { numFormat, dateFormat } from '@/utils/baseMixins'

const props = defineProps({
  contract: { type: Object, default: null },
  order: { type: Object, default: null },
  commit: { type: Number, default: 0 },
  price: { type: Number, default: 0 },
  numDown: { type: Number, default: 0 },
  numMid: { type: Number, default: 0 },
  paymentList: { type: Array, default: () => [] },
})

const dueDate = computed(
  () => props.order.extra_due_date || props.order.pay_due_date || '-',
)

const paidByOrder = computed(() => {
  const paid = props.paymentList
    .filter((p: any) => !!p.installment_order)
    .filter((p: any) => p.installment_order.pk === props.order.pk)
    .map((p: any) => p.income)
  return paid.length === 0 ? 0 : paid.reduce((x: any, y: any) => x + y)
})

const calculated = computed(() => {
  const today = dateFormat(new Date())
  const duePay = paidByOrder.value - props.commit
  return dueDate.value !== '-' && dueDate.value <= today ? duePay : 0
})
const calcClass = () => {
  let calc = calculated.value > 0 ? 'text-primary' : 'text-danger'
  return calculated.value === 0 ? '' : calc
}
</script>

<template>
  <CTableDataCell class="text-center">
    {{ dueDate }}
  </CTableDataCell>
  <CTableDataCell class="text-center">
    {{ order.pay_name }}
  </CTableDataCell>
  <CTableDataCell>
    {{ numFormat(Math.ceil(commit)) }}
  </CTableDataCell>
  <CTableDataCell :class="paidByOrder > 0 ? 'text-primary' : ''">
    {{ numFormat(paidByOrder) }}
  </CTableDataCell>
  <CTableDataCell :class="calcClass">
    {{ numFormat(calculated) }}
  </CTableDataCell>
</template>
