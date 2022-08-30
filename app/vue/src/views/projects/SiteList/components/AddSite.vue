<script lang="ts" setup>
import { ref } from 'vue'
import { write_project_cash } from '@/utils/pageAuth'
import { headerSecondary } from '@/utils/cssMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteForm from './SiteForm.vue'

defineProps({ project: { type: Number, default: null } })
const emit = defineEmits(['multi-submit'])

const formModal = ref()
const alertModal = ref()

const createConfirm = () => {
  if (write_project_cash) formModal.value.callModal()
  else alertModal.value.callModal()
}
const multiSubmit = (payload: any) => emit('multi-submit', payload)
</script>

<template>
  <CAlert :color="headerSecondary" class="text-right">
    <CButton color="primary" :disabled="!project" @click="createConfirm">
      신규등록
    </CButton>
  </CAlert>

  <FormModal ref="formModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      사업 부지 등록
    </template>
    <template #default>
      <SiteForm @multi-submit="multiSubmit" @close="formModal.close()" />
    </template>
  </FormModal>

  <AlertModal ref="alertModal" />
</template>
