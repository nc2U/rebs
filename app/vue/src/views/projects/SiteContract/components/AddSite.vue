<script lang="ts" setup>
import { ref } from 'vue'
import { SiteContract } from '@/store/types/project'
import { write_project_cash } from '@/utils/pageAuth'
import { headerLight } from '@/utils/cssMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteContractForm from './SiteContractForm.vue'

defineProps({ project: { type: Number, default: null } })
const emit = defineEmits(['multi-submit'])

const formModal = ref()
const alertModal = ref()

const createConfirm = () => {
  if (write_project_cash) formModal.value.callModal()
  else alertModal.value.callModal()
}
const multiSubmit = (payload: SiteContract) => emit('multi-submit', payload)
</script>

<template>
  <CAlert :color="headerLight" variant="solid" class="text-right">
    <CButton color="primary" :disabled="!project" @click="createConfirm">
      부지 매입계약 신규등록
    </CButton>
  </CAlert>

  <FormModal ref="formModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      부지 매입 계약 등록
    </template>
    <template #default>
      <SiteContractForm
        :project="project"
        @multi-submit="multiSubmit"
        @close="formModal.close()"
      />
    </template>
  </FormModal>

  <AlertModal ref="alertModal" />
</template>
