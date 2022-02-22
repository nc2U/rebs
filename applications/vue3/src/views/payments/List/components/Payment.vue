<template>
  <CTableRow class="text-center" v-if="payment.contract">
    <CTableDataCell>{{ payment.deal_date }}</CTableDataCell>
    <CTableDataCell>{{ payment.contract.order_group || '' }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <CIcon
        name="cib-node-js"
        :style="`color: ${payment.contract.unit_type.color || ''}`"
        size="sm"
        class="mr-1"
      />
      {{ payment.contract.unit_type.name || '' }}
    </CTableDataCell>
    <CTableDataCell>{{ payment.contract.serial_number || '' }}</CTableDataCell>
    <CTableDataCell>
      <router-link to="#">{{ payment.contract.contractor || '' }}</router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      <router-link to="#">{{ numFormat(payment.income) }}</router-link>
    </CTableDataCell>
    <CTableDataCell>{{ payment.installment_order }}</CTableDataCell>
    <CTableDataCell>{{ payment.bank_account }}</CTableDataCell>
    <CTableDataCell>{{ payment.trader }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="success" @click="updatePayment" size="sm"> 수정</CButton>
      <CButton color="danger" @click="deletePayment" size="sm"> 삭제</CButton>
    </CTableDataCell>
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
  methods: {
    updatePayment() {
      alert('수정 ok..')
    },
    deletePayment() {
      alert('삭제 ok..')
    },
  },
})
</script>
