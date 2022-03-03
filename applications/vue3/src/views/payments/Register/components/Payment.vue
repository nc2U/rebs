<template>
  <CTableRow
    class="text-center"
    :color="payment.pk === paymentId ? 'warning' : ''"
  >
    <CTableDataCell>{{ payment.deal_date }}</CTableDataCell>
    <CTableDataCell>{{ payment.installment_order }}</CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(payment.income) }}
    </CTableDataCell>
    <CTableDataCell>{{ payment.bank_account }}</CTableDataCell>
    <CTableDataCell>{{ payment.trader }}</CTableDataCell>
    <CTableDataCell>
      <CButton type="button" color="info" size="sm" @click="showDetail"
        >보기
      </CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal size="lg" ref="updateFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      건별 수납 관리
    </template>
    <template v-slot:default>
      <PaymentForm
        @on-submit="updateConfirm"
        @on-delete="deleteConfirm"
        @close="$refs.updateFormModal.visible = false"
        :payment="payment"
      />
    </template>
  </FormModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import PaymentForm from '@/views/payments/Register/components/PaymentForm.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Payment',
  components: { FormModal, PaymentForm },
  props: { payment: Object },
  computed: {
    ...mapState('payment', ['paymentId']),
  },
  methods: {
    showDetail(this: any) {
      this.$refs.updateFormModal.callModal()
    },
  },
})
</script>
