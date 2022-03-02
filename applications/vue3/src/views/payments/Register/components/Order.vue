<template>
  <CTableDataCell class="text-center">
    {{ order.extra_due_date || order.pay_due_date || '-' }}
  </CTableDataCell>
  <CTableDataCell class="text-center">{{ order.pay_name }}</CTableDataCell>
  <CTableDataCell>
    {{ numFormat(commitment) }}
  </CTableDataCell>
  <CTableDataCell>24,150,000</CTableDataCell>
  <CTableDataCell>-2,650,000</CTableDataCell>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Order',
  components: {},
  props: { contract: Object, order: Object, price: Number },
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
      const downPay = this.downPayList
        .filter((d: any) => d.order_group === this.contract.order_group.pk)
        .filter((d: any) => d.unit_type === this.contract.unit_type.pk)
        .map((d: any) => d.payment_amount)[0] // 1. downPayList, 2. payByOrder, 3. 분양가 / 총회차수
      const payByOrder = this.price * this.order.pay_ratio // 1. payByOrder
      const balacePay = 1 // 분양가 - (계약금 + 중도금), 2. payByOrder

      if (this.order.pay_sort === '1') {
        return 1 // 계약금
      } else if (this.order.pay_sort === '2') {
        return 2 // 중도금
      } else if (this.order.pay_sort === '3') {
        return 3 // 잔금
      }
    },
    ...mapState('payment', ['downPayList']),
  },
  methods: {},
})
</script>
