<script lang="ts" setup>
import { ref } from 'vue'
import { CashBook } from '@/store/types/comCash'
import { headerLight } from '@/utils/cssMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import CashForm from '@/views/comCash/CashManage/components/CashForm.vue'

const emit = defineEmits(['multi-submit'])

const createFormModal = ref()

const createConfirm = () => createFormModal.value.callModal()

const multiSubmit = (payload: {
  formData: CashBook
  sepData: CashBook | null
}) => emit('multi-submit', payload)
</script>

<template>
  <CAlert :color="headerLight" variant="solid" class="text-right">
    <CButton color="primary" @click="createConfirm">신규등록</CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>본사 입출금 거래 건별 등록</template>
    <template #default>
      <CashForm @multi-submit="multiSubmit" @close="createFormModal.close()" />
    </template>
  </FormModal>
</template>
