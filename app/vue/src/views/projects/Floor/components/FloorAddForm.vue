<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

defineProps({ disabled: Boolean })
const emit = defineEmits(['on-submit'])

const alertModal = ref()
const confirmModal = ref()

const form = reactive({
  start_floor: '',
  end_floor: '',
  extra_cond: '',
  alias_name: '',
})

const validated = ref(false)

const onSubmit = (event: any) => {
  if (write_project) {
    const el = event.currentTarget
    if (el.checkValidity() === false) {
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
  confirmModal.value.visible = false
  resetForm()
}

const resetForm = () => {
  form.start_floor = ''
  form.end_floor = ''
  form.extra_cond = ''
  form.alias_name = ''
}
</script>

<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2">
      <CCol md="2" class="mb-2">
        <CFormInput
          v-model.number="form.start_floor"
          placeholder="시작 층"
          type="number"
          min="0"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model.number="form.end_floor"
          placeholder="종료 층"
          type="number"
          min="0"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model="form.extra_cond"
          placeholder="방향/위치(옵션)"
          :disabled="disabled"
        />
      </CCol>

      <CCol md="2" class="mb-2">
        <CFormInput
          v-model="form.alias_name"
          placeholder="층별 범위 명칭"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="2" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" type="submit" :disabled="disabled">
          층별타입추가
        </CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-info" />
      층별 타입 등록
    </template>
    <template #default>
      프로젝트의 층별 범위 타입 정보 등록을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
