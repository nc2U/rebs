<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { write_contract } from '@/utils/pageAuth'
import FormModal from '@/components/Modals/FormModal.vue'
import ReleaseForm from '@/views/contracts/Release/components/ReleaseForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({ contractor: { type: Object, default: null } })
const emit = defineEmits(['on-submit'])

const releaseFormModal = ref()
const releaseAlertModal = ref()

const store = useStore()

const contRelease = computed(() => store.state.contract.contRelease)

const callFormModal = () => {
  if (write_contract) releaseFormModal.value.callModal()
  else releaseAlertModal.value.callModal()
}

const onSubmit = (payload: any) => {
  emit('on-submit', payload)
  releaseFormModal.value.visible = false
}
</script>

<template>
  <CAlert color="secondary">
    <CButton
      :color="contRelease && contRelease.pk ? 'warning' : 'danger'"
      @click="callFormModal"
    >
      {{ contRelease && contRelease.pk ? '수정하기' : '등록하기' }}
    </CButton>
  </CAlert>

  <FormModal ref="releaseFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      계약 해지 신규 등록
    </template>
    <template #default>
      <ReleaseForm
        :contractor="contractor"
        :release="contRelease"
        @on-submit="onSubmit"
        @close="$refs.releaseFormModal.visible = false"
      />
    </template>
  </FormModal>

  <AlertModal ref="releaseAlertModal" />
</template>
