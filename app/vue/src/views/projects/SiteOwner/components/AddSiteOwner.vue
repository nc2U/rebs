<script lang="ts" setup>
import { ref } from 'vue'
import { SiteOwner } from '@/store/types/project'
import { write_project } from '@/utils/pageAuth'
import { AlertLight } from '@/utils/cssMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteOwnerForm from '@/views/projects/SiteOwner/components/SiteOwnerForm.vue'

defineProps({ project: { type: Number, default: null } })
const emit = defineEmits(['multi-submit'])

const formModal = ref()
const alertModal = ref()

const createConfirm = () => {
  if (write_project.value) formModal.value.callModal()
  else alertModal.value.callModal()
}

const multiSubmit = (payload: SiteOwner) => emit('multi-submit', payload)
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="text-right">
    <CButton color="primary" :disabled="!project" @click="createConfirm">
      부지 소유자 신규등록
    </CButton>
  </CAlert>

  <FormModal ref="formModal" size="lg">
    <template #header>부지 소유자 정보 등록</template>
    <template #default>
      <SiteOwnerForm @multi-submit="multiSubmit" @close="formModal.close()" />
    </template>
  </FormModal>

  <AlertModal ref="alertModal" />
</template>
