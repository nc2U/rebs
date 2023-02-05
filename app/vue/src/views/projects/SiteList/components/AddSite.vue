<script lang="ts" setup>
import { ref } from 'vue'
import { Site } from '@/store/types/project'
import { write_project } from '@/utils/pageAuth'
import { AlertLight } from '@/utils/cssMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteForm from './SiteForm.vue'

defineProps({ project: { type: Number, default: null } })
const emit = defineEmits(['multi-submit'])

const formModal = ref()
const alertModal = ref()

const createConfirm = () => {
  if (write_project.value) formModal.value.callModal()
  else alertModal.value.callModal()
}
const multiSubmit = (payload: Site) => emit('multi-submit', payload)
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="text-right">
    <CButton color="primary" :disabled="!project" @click="createConfirm">
      사업 부지 신규등록
    </CButton>
  </CAlert>

  <FormModal ref="formModal" size="lg">
    <template #header>사업 부지 등록</template>
    <template #default>
      <SiteForm @multi-submit="multiSubmit" @close="formModal.close()" />
    </template>
  </FormModal>

  <AlertModal ref="alertModal" />
</template>
