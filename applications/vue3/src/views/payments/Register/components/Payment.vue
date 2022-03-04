<template>
  <CTableRow
    class="text-center"
    :color="payment.pk.toString() === paymentId ? 'warning' : ''"
  >
    <CTableDataCell>{{ payment.deal_date }}</CTableDataCell>
    <CTableDataCell>{{ payment.installment_order.__str__ }}</CTableDataCell>
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
        @on-submit="updateConfirm"
        @on-delete="deleteConfirm"
        @close="$refs.updateFormModal.visible = false"
        :payment="payment"
      />
    </template>
  </FormModal>

  <ConfirmModal ref="delModal">
    <template v-slot:header>
      <CIcon name="cilWarning" />
      건별 수납 정보 삭제
    </template>
    <template v-slot:default>
      삭제한 데이터는 복구할 수 없습니다. 해당 건별 수납 정보를
      삭제하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import PaymentForm from '@/views/payments/Register/components/PaymentForm.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'Payment',
  components: { FormModal, PaymentForm, ConfirmModal, AlertModal },
  props: { payment: Object, paymentId: String, contract: Object },
  mounted(this: any) {
    if (this.paymentId === this.payment.pk.toString()) {
      this.showDetail()
    }
  },
  computed: {
    pageManageAuth() {
      return (
        this.superAuth || (this.staffAuth && this.staffAuth.payment === '2')
      )
    },
    allowedPeriod(this: any) {
      return this.superAuth || this.diffDate(this.payment.deal_date) <= 90
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    showDetail(this: any) {
      this.$refs.updateFormModal.callModal()
    },
    updateConfirm(this: any, payload: any) {
      if (this.pageManageAuth)
        if (this.allowedPeriod) this.updateObject(payload)
        else
          this.$refs.alertModal.callModal(
            null,
            '수납일로부터 90일이 경과한 건은 수정할 수 없습니다. 관리자에게 문의바랍니다.',
          )
      else this.$refs.alertModal.callModal()
    },
    updateObject(this: any, payload: any) {
      this.$emit('on-update', { ...{ pk: this.payment.pk }, ...payload })
      this.$refs.updateFormModal.visible = false
    },
    deleteConfirm(this: any) {
      if (this.pageManageAuth)
        if (this.allowedPeriod) this.$refs.delModal.callModal()
        else
          this.$refs.alertModal.callModal(
            null,
            '수납일로부터 90일이 경과한 건은 삭제할 수 없습니다. 관리자에게 문의바랍니다.',
          )
      else this.$refs.alertModal.callModal()
    },
    deleteObject(this: any) {
      this.$emit('on-delete', this.payment.pk)
      this.$refs.delModal.visible = false
    },
  },
})
</script>
