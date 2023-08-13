<script lang="ts" setup>
import { computed, type PropType } from 'vue'
import { type AllPayment, type PayOrder } from '@/store/types/payment'
import { numFormat, getToday } from '@/utils/baseMixins'

const props = defineProps({
  contract: { type: Object, default: null },
  order: { type: Object as PropType<PayOrder>, default: null },
  commit: { type: Number, default: 0 },
  price: { type: Number, default: 0 },
  numDown: { type: Number, default: 0 },
  numMid: { type: Number, default: 0 },
  paymentList: { type: Array as PropType<AllPayment[]>, default: () => [] },
})

const dueDate = computed(() => props.order.extra_due_date || props.order.pay_due_date || '-')

const paidByOrder = computed(() => {
  const paid = props.paymentList
    .filter((p: AllPayment) => !!p.installment_order)
    .filter(p => p.installment_order.pk === props.order.pk)
    .map(p => p.income)

  return paid.length === 0 ? 0 : paid.reduce((x: number, y: number) => x + y, 0)
})

const calculated = computed(() => {
  const duePay = paidByOrder.value - props.commit
  return dueDate.value !== '-' && dueDate.value <= getToday() ? duePay : 0
})
const calcClass = () => {
  const calc = calculated.value > 0 ? 'text-primary' : 'text-danger'
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
