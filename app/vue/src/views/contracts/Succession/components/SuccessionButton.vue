<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { Succession } from '@/store/types/contract'
import { AlertLight } from '@/utils/cssMixins'
import { write_contract } from '@/utils/pageAuth'
import FormModal from '@/components/Modals/FormModal.vue'
import SuccessionForm from '@/views/contracts/Succession/components/SuccessionForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const emit = defineEmits(['on-submit'])

const successionFormModal = ref()
const successionAlertModal = ref()

const contractStore = useContract()
const succession = computed(() => contractStore.succession)

const isSuccession = computed(
  () => !!succession.value && !succession.value.is_approval,
)

const callFormModal = () => {
  if (write_contract.value) successionFormModal.value.callModal()
  else successionAlertModal.value.callModal()
}

const onSubmit = (payload: Succession) => {
  emit('on-submit', payload)
  successionFormModal.value.close()
}
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="text-right">
    <CButton
      :color="isSuccession ? 'success' : 'primary'"
      @click="callFormModal"
    >
      {{ isSuccession ? '수정하기' : '등록하기' }}
    </CButton>
  </CAlert>

  <FormModal ref="successionFormModal" size="lg">
    <template #header>
      권리 의무 승계 {{ isSuccession ? '수정' : '신규' }} 등록
    </template>
    <template #default>
      <SuccessionForm
        :succession="isSuccession ? (succession as Succession) : undefined"
        @on-submit="onSubmit"
        @close="successionFormModal.close()"
      />
    </template>
  </FormModal>

  <AlertModal ref="successionAlertModal" />
</template>
