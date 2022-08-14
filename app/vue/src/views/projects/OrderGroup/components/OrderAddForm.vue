<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({ disabled: Boolean })
const emit = defineEmits(['on-submit'])

const alertModal = ref()
const confirmModal = ref()

const validated = ref(false)
const form = reactive({
  order_number: null,
  sort: '',
  order_group_name: '',
})

const onSubmit = (event: any) => {
  if (write_project) {
    const e = event.currentTarget
    if (e.checkValidity() === false) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else confirmModal.value.callModal()
  } else {
    alertModal.value.callModal()
    resetForm()
  }
}

const modalAction = () => {
  emit('on-submit', form)
  validated.value = false
  confirmModal.value.visible = false
  resetForm()
}

const resetForm = () => {
  form.order_number = null
  form.sort = ''
  form.order_group_name = ''
}
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
          v-model.number="form.order_number"
          placeholder="등록차수"
          type="number"
          min="1"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormSelect v-model="form.sort" :disabled="disabled" required>
          <option value="">구분선택</option>
          <option value="1">일반분양</option>
          <option value="2">조합모집</option>
        </CFormSelect>
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="form.order_group_name"
          placeholder="차수그룹명"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="3" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" type="submit" :disabled="disabled">
          그룹추가
        </CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-info" />
      차수그룹 등록
    </template>
    <template #default>
      프로젝트의 차수그룹 정보 등록을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
