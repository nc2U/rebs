<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({ disabled: Boolean })
const emit = defineEmits(['on-submit'])

const alertModal = ref()
const confirmModal = ref()

const form = reactive({ name: '' })
const validated = ref(false)

const onSubmit = (event: Event) => {
  if (write_project.value) {
    const form = event.currentTarget as HTMLFormElement
    if (!form.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else {
      confirmModal.value.callModal()
    }
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}
const modalAction = () => {
  emit('on-submit', form)
  validated.value = false
  confirmModal.value.close()
  resetForm()
}
const resetForm = () => (form.name = '')
</script>

<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2" color="success">
      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.name"
          maxlength="10"
          placeholder="동(건물) 이름"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="3" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" type="submit" :disabled="disabled">
          동 추가
        </CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header> 동(건물) 등록 </template>
    <template #default>
      프로젝트의 동(건물) 정보 등록을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
