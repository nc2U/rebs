<script lang="ts" setup>
import { ref } from 'vue'
import { AlertLight } from '@/utils/cssMixins'
import { ProBankAcc, ProjectCashBook } from '@/store/types/proCash'
import FormModal from '@/components/Modals/FormModal.vue'
import ProImprestForm from '@/views/proCash/Imprest/components/ProImprestForm.vue'

defineProps({ project: { type: Number, default: null } })
const emit = defineEmits(['multi-submit', 'on-bank-update'])

const createFormModal = ref()

const createConfirm = () => createFormModal.value.callModal()

const multiSubmit = (payload: {
  formData: ProjectCashBook
  sepData: ProjectCashBook | null
}) => emit('multi-submit', payload)

const onBankUpdate = (payload: ProBankAcc) => emit('on-bank-update', payload)
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="text-right">
    <CButton color="primary" :disabled="!project" @click="createConfirm">
      신규등록
    </CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>운영비(전도금) 거래 건별 등록</template>
    <template #default>
      <ProImprestForm
        @multi-submit="multiSubmit"
        @onBankUpdate="onBankUpdate"
        @close="createFormModal.close()"
      />
    </template>
  </FormModal>
</template>
