<script lang="ts" setup>
import { ref } from 'vue'
import { write_project_cash } from '@/utils/pageAuth'
import FormModal from '@/components/Modals/FormModal.vue'
import ProCashForm from '@/views/proCash/Manage/components/ProCashForm.vue'
import { headerSecondary } from '@/utils/cssMixins'

const emit = defineEmits(['multi-submit'])

const createFormModal = ref()
const createAlertModal = ref()

const createConfirm = () => {
  if (write_project_cash) createFormModal.value.callModal()
  else createAlertModal.value.callModal()
}
const multiSubmit = (payload: any) => emit('multi-submit', payload)
</script>

<template>
  <CAlert :color="headerSecondary" class="text-right">
    <CButton color="primary" @click="createConfirm">신규등록</CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      프로젝트 입출금 거래 건별 등록
    </template>
    <template #default>
      <ProCashForm
        @multi-submit="multiSubmit"
        @close="createFormModal.close()"
      />
    </template>
  </FormModal>

  <AlertModal ref="createAlertModal" />
</template>
