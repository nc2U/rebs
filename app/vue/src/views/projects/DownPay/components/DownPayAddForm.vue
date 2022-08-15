<script lang="ts" setup>
import { ref, reactive, watch } from 'vue'
import { write_project } from '@/utils/pageAuth'
import { isValidate } from '@/utils/helper'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  disabled: Boolean,
  orders: { type: Array, default: [] },
  types: { type: Array, default: [] },
})
const emit = defineEmits(['on-submit'])

const alertModal = ref()
const confirmModal = ref()

const form = reactive({
  order_group: '',
  unit_type: '',
  number_payments: null,
  payment_amount: null,
})

const validated = ref(false)

watch(props, () => {
  form.order_group = ''
  form.unit_type = ''
})

const onSubmit = (event: any) => {
  if (write_project) {
    isValidate(event)
      ? (validated.value = true)
      : confirmModal.value.callModal()
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}
const modalAction = () => {
  emit('on-submit', form)
  validated.value = false
  confirmModal.value.visible = false
  resetForm()
}
const resetForm = () => {
  form.order_group = ''
  form.unit_type = ''
  form.number_payments = null
  form.payment_amount = null
}
</script>

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
          <option v-for="order in orders" :key="order.pk" :value="order.pk">
            {{ order.order_group_name }}
          </option>
        </CFormSelect>
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormSelect v-model="form.unit_type" :disabled="disabled" required>
          <option value="">타입선택</option>
          <option v-for="type in types" :key="type.pk" :value="type.pk">
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
            <CButton color="primary" type="submit" :disabled="disabled">
              계약금 추가
            </CButton>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-info" />
      타입별 계약금
    </template>
    <template #default>
      프로젝트의 타입별 계약금 정보 등록을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
