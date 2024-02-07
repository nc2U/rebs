<script lang="ts" setup>
import { inject, reactive, ref } from 'vue'
import { write_project } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

export type SortType = {
  value: '1' | '2' | '3' | '4' | '5' | '6'
  label: string
}

const typeSort = inject<SortType[]>('typeSort')
defineProps({ disabled: Boolean })
const emit = defineEmits(['on-submit'])

const refAlertModal = ref()
const refConfirmModal = ref()

const validated = ref(false)
const form = reactive({
  sort: '',
  name: '',
  color: '',
  actual_area: null,
  supply_area: null,
  contract_area: null,
  average_price: null,
  num_unit: null,
})

const onSubmit = (event: Event) => {
  if (write_project.value) {
    const el = event.currentTarget as HTMLFormElement
    if (!el.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()

      validated.value = true
    } else {
      refConfirmModal.value.callModal()
    }
  } else {
    refAlertModal.value.callModal()
    resetForm()
  }
}

const modalAction = () => {
  emit('on-submit', form)
  validated.value = false
  refConfirmModal.value.close()
  resetForm()
}

const resetForm = () => {
  form.sort = ''
  form.name = ''
  form.color = ''
  form.actual_area = null
  form.supply_area = null
  form.contract_area = null
  form.average_price = null
  form.num_unit = null
}
</script>

<template>
  <CForm novalidate class="needs-validation" :validated="validated" @submit.prevent="onSubmit">
    <CRow class="p-2">
      <CCol lg="7">
        <CRow>
          <CCol lg="3" class="mb-2">
            <CFormSelect v-model="form.sort" required :disabled="disabled">
              <option value="">타입</option>
              <option v-for="tp in typeSort" :key="tp.value" :value="tp.value">
                {{ tp.label }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol lg="3" class="mb-2">
            <CFormInput
              v-model="form.name"
              maxlength="10"
              placeholder="옵션 코드"
              required
              :disabled="disabled"
            />
          </CCol>

          <CCol lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.actual_area"
              placeholder="옵션 명칭"
              :disabled="disabled"
            />
            <CFormFeedback invalid> 전용면적을 소소점4자리 이하로 입력하세요.</CFormFeedback>
          </CCol>

          <CCol lg="3" class="mb-2">
            <CFormInput
              v-model.number="form.supply_area"
              placeholder="옵션 가격"
              type="number"
              min="0"
              :disabled="disabled"
            />
            <CFormFeedback invalid> 공급면적을 소소점4자리 이하로 입력하세요.</CFormFeedback>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="5">
        <CRow>
          <CCol lg="9" class="mb-2">
            <CFormInput
              v-model.number="form.contract_area"
              placeholder="상세 설명"
              :disabled="disabled"
            />
            <CFormFeedback invalid> 계약면적을 소소점4자리 이하로 입력하세요.</CFormFeedback>
          </CCol>

          <CCol lg="3" class="d-grid gap-2 d-lg-block mb-3">
            <CButton color="primary" type="submit" :disabled="disabled"> 옵션추가</CButton>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CForm>

  <ConfirmModal ref="refConfirmModal">
    <template #header> 타입 정보 등록</template>
    <template #default> 프로젝트의 타입 정보 등록을 진행하시겠습니까?</template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="refAlertModal" />
</template>
