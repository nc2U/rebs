<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2">
      <CCol md="2" class="mb-2">
        <CFormSelect v-model="form.order_group" :disabled="disabled" required>
          <option value="">차수선택</option>
          <option v-for="order in orders" :value="order.pk" :key="order.pk">
            {{ order.order_group_name }}
          </option>
        </CFormSelect>
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormSelect v-model="form.unit_type" :disabled="disabled" required>
          <option value="">타입선택</option>
          <option v-for="type in types" :value="type.pk" :key="type.pk">
            {{ type.name }}
          </option>
        </CFormSelect>
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model.number="form.number_payments"
          placeholder="분할 납부회수"
          type="number"
          min="0"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model.number="form.payment_amount"
          placeholder="납부 계약금액"
          type="number"
          min="0"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="2">
        <CRow>
          <CCol md="12" class="d-grid gap-2 d-lg-block mb-3">
            <CButton color="primary" :disabled="disabled">계약금 추가</CButton>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-info" />
      타입별 계약금
    </template>
    <template v-slot:default>
      프로젝트의 타입별 계약금 정보 등록을 진행하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import { maska } from 'maska'

export default defineComponent({
  name: 'DownPayAddForm',
  directives: { maska },
  components: { ConfirmModal },
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
  props: ['disabled', 'orders', 'types'],
  methods: {
    onSubmit(this: any, event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        this.validated = true
      } else {
        this.$refs.confirmModal.callModal()
      }
    },
    modalAction(this: any) {
      this.$emit('on-submit', this.form)
      this.validated = false
      this.$refs.confirmModal.visible = false
      this.resetForm()
    },
    resetForm() {
      this.form.order_group = null
      this.form.unit_type = null
      this.form.number_payments = null
      this.form.payment_amount = null
    },
  },
})
</script>
