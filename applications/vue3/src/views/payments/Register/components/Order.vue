<template>
  <CTableDataCell class="text-center">
    {{ order.extra_due_date || order.pay_due_date || '-' }}
  </CTableDataCell>
  <CTableDataCell class="text-center">{{ order.pay_name }}</CTableDataCell>
  <CTableDataCell>
    {{ numFormat(commitment) }}
  </CTableDataCell>
  <CTableDataCell class="text-danger">24,150,000</CTableDataCell>
  <CTableDataCell class="text-danger">-2,650,000</CTableDataCell>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Order',
  components: {},
  props: {
    contract: Object,
    order: Object,
    price: Number,
    numDown: Number,
    numMid: Number,
  },
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {
    commitment(this: any) {
      const down = this.downPayList
        .filter((d: any) => d.order_group === this.contract.order_group.pk)
        .filter((d: any) => d.unit_type === this.contract.unit_type.pk)
        .map((d: any) => d.payment_amount)[0] // 1. downPayList, 2. payByOrder, 3. 분양가 / 총회차수
      const payByOrder = this.order.pay_ratio
        ? this.price * this.order.pay_ratio
        : this.price * 0.1 // 1. payByOrder
      const downPay = down ? down : payByOrder
      const numDown = this.numDown // 계약금 납부회수
      const numMid = this.numMid // 중도금 납부회수
      const balace = this.price - downPay * numDown - payByOrder * numMid // 분양가 - (계약금 + 중도금), 2. payByOrder
      const balacePay = balace ? balace : payByOrder * this.order.pay_ratio

      if (this.order.pay_sort === '1') {
        return downPay // 계약금
      } else if (this.order.pay_sort === '2') {
        return payByOrder // 중도금
      } else if (this.order.pay_sort === '3') {
        return balacePay // 잔금
      } else return 0
    },
    ...mapState('payment', ['downPayList']),
  },
  methods: {},
})
</script>
