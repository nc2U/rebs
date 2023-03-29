<script lang="ts" setup>
import { ref } from 'vue'
import { AlertLight } from '@/utils/cssMixins'
import { ProBankAcc, ProjectCashBook } from '@/store/types/proCash'
import FormModal from '@/components/Modals/FormModal.vue'
import ProCashForm from '@/views/proCash/Manage/components/ProCashForm.vue'

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
    <CButton color="primary" @click="createConfirm">신규등록</CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>프로젝트 입출금 거래 건별 등록</template>
    <template #default>
      <ProCashForm
        @multi-submit="multiSubmit"
        @onBankUpdate="onBankUpdate"
        @close="createFormModal.close()"
      />
    </template>
  </FormModal>
</template>
