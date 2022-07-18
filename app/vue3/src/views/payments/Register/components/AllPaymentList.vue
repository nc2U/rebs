<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="16%" />
      <col width="18%" />
      <col width="16%" />
      <col width="22%" />
      <col width="18%" />
      <col width="10%" />
    </colgroup>

    <CTableHead color="secondary">
      <CTableRow class="text-center">
        <CTableHeaderCell>수납일자</CTableHeaderCell>
        <CTableHeaderCell>납부회차</CTableHeaderCell>
        <CTableHeaderCell>수납금액</CTableHeaderCell>
        <CTableHeaderCell>수납계좌</CTableHeaderCell>
        <CTableHeaderCell>입금자명</CTableHeaderCell>
        <CTableHeaderCell>비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody v-if="contract">
      <Payment
        v-for="pay in paymentList"
        :contract="contract"
        :payment-id="paymentId"
        :payment="pay"
        :key="pay.pk"
        @on-update="onUpdate"
        @on-delete="onDelete"
      />
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right">
        <CTableHeaderCell color="secondary" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell>
          {{ numFormat(paymentSum) }}
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Payment from '@/views/payments/Register/components/Payment.vue'

export default defineComponent({
  name: 'AllPaymentList',
  components: { Payment },
  props: { contract: Object, paymentList: Array, paymentId: String },
  computed: {
    paymentSum(this: any) {
      return this.paymentList.length !== 0
        ? this.paymentList
            .map((p: any) => p.income)
            .reduce((x: any, y: any) => x + y)
        : 0
    },
  },
  methods: {
    onUpdate(payload: any) {
      this.$emit('on-update', payload)
    },
    onDelete(pk: number) {
      this.$emit('on-delete', pk)
    },
  },
})
</script>
