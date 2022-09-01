<script lang="ts" setup>
import { ref } from 'vue'
import { write_project_cash } from '@/utils/pageAuth'
import { headerLight } from '@/utils/cssMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteOwnerForm from '@/views/projects/SiteOwner/components/SiteOwnerForm.vue'

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
  <CAlert :color="headerLight" variant="solid" class="text-right">
    <CButton color="primary" :disabled="!project" @click="createConfirm">
      부지 소유자 신규등록
    </CButton>
  </CAlert>

  <FormModal ref="formModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      부지 소유자 정보 등록
    </template>
    <template #default>
      <SiteOwnerForm @multi-submit="multiSubmit" @close="formModal.close()" />
    </template>
  </FormModal>

  <AlertModal ref="alertModal" />
</template>
