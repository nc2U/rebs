<template>
  <CTableRow
    class="text-center"
    :color="payment.pk.toString() === paymentId ? 'secondary' : ''"
  >
    <CTableDataCell>{{ payment.deal_date }}</CTableDataCell>
    <CTableDataCell>
      {{ payment.installment_order ? payment.installment_order.__str__ : '-' }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      <router-link to="" @click="showDetail">
        {{ numFormat(payment.income) }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>{{ payment.bank_account.alias_name }}</CTableDataCell>
    <CTableDataCell>{{ payment.trader }}</CTableDataCell>
    <CTableDataCell>
      <CButton type="button" color="info" size="sm" @click="showDetail">
        보기
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
        :contract="contract"
        @on-submit="updateObject"
        @on-delete="deleteObject"
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
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'Payment',
  components: { FormModal, PaymentForm },
  props: { payment: Object, paymentId: String, contract: Object },
  mounted(this: any) {
    if (this.paymentId === this.payment.pk.toString()) {
      this.showDetail()
    }
  },
  computed: {
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    showDetail(this: any) {
      this.$refs.updateFormModal.callModal()
    },
    updateObject(this: any, payload: any) {
      this.$emit('on-update', { ...{ pk: this.payment.pk }, ...payload })
      this.$refs.updateFormModal.visible = false
    },
    deleteObject(this: any) {
      this.$emit('on-delete', this.payment.pk)
    },
  },
})
</script>
