<script lang="ts" setup="">
import { ref } from 'vue'
import { AlertSecondary } from '@/utils/cssMixins'
import { write_human_resource } from '@/utils/pageAuth'
import FormModal from '@/components/Modals/FormModal.vue'
import RankForm from './RankForm.vue'

const formModal = ref()
const alertModal = ref()

const createConfirm = () => {
  if (write_human_resource.value) formModal.value.callModal()
  else alertModal.value.callModal()
}
</script>

<template>
  <CAlert :color="AlertSecondary" class="text-right">
    <CButton color="primary" @click="createConfirm">직급 정보 신규등록</CButton>
  </CAlert>

  <FormModal ref="formModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      직급 정보 등록
    </template>
    <template #default>
      <RankForm @close="formModal.close()" />
    </template>
  </FormModal>

  <AlertModal ref="alertModal" />
</template>
