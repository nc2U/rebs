<script lang="ts" setup>
import { ref, reactive, computed, onBeforeMount } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  downPay: { type: Object, default: null },
  orders: { type: Array, default: () => [] },
  types: { type: Array, default: () => [] },
})
const emit = defineEmits(['on-update', 'on-delete'])

const form = reactive({
  order_group: null,
  unit_type: null,
  payment_amount: null,
})

const alertModal = ref()
const confirmModal = ref()

onBeforeMount(() => {
  if (props.downPay) resetForm()
})

const formsCheck = computed(() => {
  if (props.downPay) {
    const a = form.order_group === props.downPay.order_group
    const b = form.unit_type === props.downPay.unit_type
    const c = form.payment_amount === props.downPay.payment_amount
    return a && b && c
  } else return false
})

const formCheck = (bool: boolean) => {
  if (bool) onUpdateDownPay()
  return
}
const onUpdateDownPay = () => {
  if (write_project.value) {
    const pk = props.downPay.pk
    emit('on-update', { ...{ pk }, ...form })
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}
const onDeleteDownPay = () => {
  if (useAccount().superAuth) confirmModal.value.callModal()
  else {
    alertModal.value.callModal()
    resetForm()
  }
}
const modalAction = () => {
  emit('on-delete', props.downPay.pk)
  confirmModal.value.close()
}

const resetForm = () => {
  form.order_group = props.downPay.order_group
  form.unit_type = props.downPay.unit_type
  form.payment_amount = props.downPay.payment_amount
}
</script>

<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect v-model="form.order_group" required>
        <option value="">차수선택</option>
        <option v-for="order in orders" :key="order.pk" :value="order.pk">
          {{ order.order_group_name }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.unit_type" required>
        <option value="">타입선택</option>
        <option v-for="type in types" :key="type.pk" :value="type.pk">
          {{ type.name }}
        </option>
      </CFormSelect>
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
        :disabled="formsCheck"
        @click="onUpdateDownPay"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteDownPay">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header> 층별 타입 삭제</template>
    <template #default>
      이 타입에 종속된 분양가 데이터가 있는 경우 해당 데이터를 모두 제거한 후
      삭제가능 합니다. 해당 층별 타입을 삭제 하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
