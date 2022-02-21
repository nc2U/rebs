<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect v-model="form.order_group" required>
        <option value="">차수선택</option>
        <option v-for="order in orders" :value="order.pk" :key="order.pk">
          {{ order.order_group_name }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.unit_type" required>
        <option value="">타입선택</option>
        <option v-for="type in types" :value="type.pk" :key="type.pk">
          {{ type.name }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.number_payments"
        placeholder="납입회차 코드"
        type="number"
        min="0"
        required
        @keypress.enter="
          formCheck(form.number_payments !== downPay.number_payments)
        "
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.payment_amount"
        placeholder="납부순서"
        type="number"
        min="0"
        required
        @keypress.enter="
          formCheck(form.payment_amount !== downPay.payment_amount)
        "
      />
    </CTableDataCell>

    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        @click="onUpdateDownPay"
        :disabled="formsCheck"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteDownPay">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-warning" />
      층별 타입 삭제
    </template>
    <template v-slot:default>
      이 타입에 종속된 분양가 데이터가 있는 경우 해당 데이터를 모두 제거한 후
      삭제가능 합니다. 해당 층별 타입을 삭제 하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'DownPay',
  components: { ConfirmModal, AlertModal },
  data() {
    return {
      form: {
        order_group: null,
        unit_type: null,
        number_payments: null,
        payment_amount: null,
      },
      validated: false,
    }
  },
  props: { downPay: Object, orders: Array, types: Array },
  created(this: any) {
    if (this.downPay) {
      this.resetForm()
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.order_group === this.downPay.order_group
      const b = this.form.unit_type === this.downPay.unit_type
      const c = this.form.number_payments === this.downPay.number_payments
      const d = this.form.payment_amount === this.downPay.payment_amount
      return a && b && c && d
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    formCheck(bool: boolean) {
      if (bool) this.onUpdateDownPay()
      return
    },
    onUpdateDownPay(this: any) {
      if (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.project === '2')
      ) {
        const pk = this.downPay.pk
        this.$emit('on-update', { ...{ pk }, ...this.form })
      } else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    onDeleteDownPay(this: any) {
      if (this.superAuth) this.$refs.confirmModal.callModal()
      else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.downPay.pk)
      this.$refs.confirmModal.visible = false
    },
    resetForm(this: any) {
      this.form.order_group = this.downPay.order_group
      this.form.unit_type = this.downPay.unit_type
      this.form.number_payments = this.downPay.number_payments
      this.form.payment_amount = this.downPay.payment_amount
    },
  },
})
</script>
