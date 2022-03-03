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

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Order',
  props: {
    contract: Object,
    order: Object,
    commit: Number,
    price: Number,
    numDown: Number,
    numMid: Number,
    paymentList: Array,
  },
  computed: {
    dueDate(this: any) {
      return this.order.extra_due_date || this.order.pay_due_date || '-'
    },
    paidByOrder(this: any) {
      const paid = this.paymentList
        .filter((p: any) => p.installment_order === this.order.__str__)
        .map((p: any) => p.income)
      return paid.length === 0 ? 0 : paid.reduce((x: any, y: any) => x + y)
    },
    calculated(this: any) {
      const today = this.dateFormat(new Date())
      const duePay = this.paidByOrder - this.commit
      return this.dueDate !== '-' && this.dueDate <= today ? duePay : 0
    },
    calcClass() {
      let calc = this.calculated > 0 ? 'text-primary' : 'text-danger'
      return this.calculated === 0 ? '' : calc
    },
    ...mapState('payment', ['downPayList']),
  },
})
</script>
