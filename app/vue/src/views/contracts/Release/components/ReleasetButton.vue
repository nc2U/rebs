<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { ContractRelease } from '@/store/types/contract'
import { AlertLight } from '@/utils/cssMixins'
import { write_contract } from '@/utils/pageAuth'
import FormModal from '@/components/Modals/FormModal.vue'
import ReleaseForm from '@/views/contracts/Release/components/ReleaseForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({ contractor: { type: Object, default: null } })
const emit = defineEmits(['on-submit'])

const releaseFormModal = ref()
const releaseAlertModal = ref()

const contractStore = useContract()
const contRelease = computed(() => contractStore.contRelease)

const callFormModal = () => {
  if (write_contract.value) releaseFormModal.value.callModal()
  else releaseAlertModal.value.callModal()
}

const onSubmit = (payload: ContractRelease) => {
  emit('on-submit', payload)
  releaseFormModal.value.close()
}
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="text-right">
    <CButton
      :color="contRelease ? 'warning' : 'danger'"
      :disabled="!!props.contractor.succession"
      @click="callFormModal"
    >
      {{ contRelease ? '수정하기' : '등록하기' }}
    </CButton>
  </CAlert>

  <FormModal ref="releaseFormModal" size="lg">
    <template #header>
      계약 해지 {{ contRelease ? '수정' : '신규' }} 등록
    </template>
    <template #default>
      <ReleaseForm
        :contractor="contractor"
        :release="contRelease"
        @on-submit="onSubmit"
        @close="releaseFormModal.close()"
      />
    </template>
  </FormModal>

  <AlertModal ref="releaseAlertModal" />
</template>
