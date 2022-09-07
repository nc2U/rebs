<script lang="ts" setup>
import { ref } from 'vue'
import { write_project_cash } from '@/utils/pageAuth'
import { headerLight } from '@/utils/cssMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import ProImprestForm from '@/views/proCash/Imprest/components/ProImprestForm.vue'

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
  <CAlert :color="headerLight" variant="solid" class="text-right">
    <CButton color="primary" @click="createConfirm">신규등록</CButton>
  </CAlert>

  <FormModal ref="createFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      운영비(전도금) 거래 건별 등록
    </template>
    <template #default>
      <ProImprestForm
        @multi-submit="multiSubmit"
        @close="createFormModal.close()"
      />
    </template>
  </FormModal>

  <AlertModal ref="createAlertModal" />
</template>
