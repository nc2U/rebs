<template>
  <CTableRow class="text-center">
    <CTableDataCell>{{ payment.deal_date }}</CTableDataCell>
    <CTableDataCell>{{ payment.contract }}</CTableDataCell>
    <CTableDataCell>{{ payment.contract }}</CTableDataCell>
    <CTableDataCell>{{ payment.contract }}</CTableDataCell>
    <CTableDataCell>
      <router-link to="#">{{ payment.contract }}</router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      <router-link to="#">{{ numFormat(payment.income) }}</router-link>
    </CTableDataCell>
    <CTableDataCell>{{ payment.installment_order }}</CTableDataCell>
    <CTableDataCell>{{ payment.bank_account }}</CTableDataCell>
    <CTableDataCell>{{ payment.trader }}</CTableDataCell>
    <CTableDataCell>수정/삭제</CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'

export default defineComponent({
  name: 'Payment',
  mixins: [commonMixin],
  props: {
    payment: {
      type: Object,
      required: true,
    },
  },
})
</script>
