<script lang="ts" setup>
import { ref, reactive, inject, watch } from 'vue'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const d1List = inject('d1List')
const d2List = inject('d2List')

const props = defineProps({ disabled: Boolean })
const emit = defineEmits(['on-submit'])

const alertModal = ref()
const confirmModal = ref()

const validated = ref(false)
const form = reactive({
  account_d1: null,
  account_d2: null,
  item_name: '',
  basis_calc: '',
  budget: null,
})

watch(props, newVal => {
  if (!!newVal.disabled) resetForm()
})

const onSubmit = (event: Event) => {
  if (write_project.value) {
    const e = event.currentTarget as HTMLFormElement
    if (!e.checkValidity()) {
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
  confirmModal.value.close()
  resetForm()
}

const resetForm = () => {
  form.account_d1 = null
  form.account_d2 = null
  form.item_name = ''
  form.basis_calc = ''
  form.budget = null
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
      <CCol md="4" lg="2" class="mb-2">
        <CFormSelect v-model="form.account_d1" required :disabled="disabled">
          <option value="">대분류</option>
          <option v-for="d1 in d1List" :key="d1.pk" :value="d1.pk">
            {{ d1.name }}
          </option>
        </CFormSelect>
      </CCol>

      <CCol md="4" lg="2" class="mb-2">
        <CFormSelect v-model="form.account_d2" :disabled="disabled">
          <option value="">중분류</option>
          <option v-for="d2 in d2List" :key="d2.pk" :value="d2.pk">
            {{ d2.name }}
          </option>
        </CFormSelect>
      </CCol>

      <CCol md="4" lg="2" class="mb-2">
        <CFormInput
          v-model="form.item_name"
          placeholder="항목명칭"
          maxlength="20"
          :disabled="disabled"
          :required="!form.account_d2"
        />
      </CCol>

      <CCol md="4" lg="2" class="mb-2">
        <CFormInput
          v-model="form.basis_calc"
          placeholder="산출근거"
          maxlength="18"
          :disabled="disabled"
        />
      </CCol>

      <CCol md="4" lg="2" class="mb-2">
        <CFormInput
          v-model.number="form.budget"
          min="0"
          placeholder="지출예산"
          type="number"
          maxlength="18"
          required
          :disabled="disabled"
        />
      </CCol>

      <CCol md="4" lg="2" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary" type="submit" :disabled="disabled">
          지출 예산 추가
        </CButton>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="confirmModal">
    <template #header> 수입 예산 등록</template>
    <template #default>
      프로젝트의 수입 예산 정보 등록을 진행하시겠습니까?
    </template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
