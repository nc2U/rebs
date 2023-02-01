<script lang="ts" setup="">
import { ref } from 'vue'
import { AlertSecondary } from '@/utils/cssMixins'
import { write_human_resource } from '@/utils/pageAuth'
import { Position } from '@/store/types/company'
import FormModal from '@/components/Modals/FormModal.vue'
import PositionForm from './PositionForm.vue'

defineProps({
  company: {
    type: String,
    default: null,
  },
})
const emit = defineEmits(['multi-submit'])

const formModal = ref()
const alertModal = ref()

const createConfirm = () => {
  if (write_human_resource.value) formModal.value.callModal()
  else alertModal.value.callModal()
}
const multiSubmit = (payload: Position) => emit('multi-submit', payload)
</script>

<template>
  <CAlert :color="AlertSecondary" class="text-right">
    <CButton color="primary" @click="createConfirm">직급 정보 신규등록</CButton>
  </CAlert>

  <FormModal ref="formModal" size="lg">
    <template #header>직급 정보 등록</template>
    <template #default>
      <PositionForm
        :company="company"
        @multi-submit="multiSubmit"
        @close="formModal.close()"
      />
    </template>
  </FormModal>

  <AlertModal ref="alertModal" />
</template>
