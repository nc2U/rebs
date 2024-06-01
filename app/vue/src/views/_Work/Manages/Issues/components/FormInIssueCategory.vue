<script lang="ts" setup>
import { ref } from 'vue'
import { isValidate } from '@/utils/helper'

const emit = defineEmits(['close'])

const validated = ref(false)

const nCategory = ref({
  name: '',
  assigned_to: null,
})

const createCategory = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    alert('created!')
    // emit('on-submit', {
    //   ...form.value,
    //   ...timeEntry.value,
    //   newFiles: newFiles.value,
    //   comment_content: comment.value.content,
    // })
    validated.value = false
  }
}

const closeModal = () => emit('close')
</script>

<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="createCategory"
  >
    <CModalBody class="text-body">
      <CRow class="mb-3">
        <CFormLabel for="category-name" class="col-3 col-form-label required text-right">
          이름
        </CFormLabel>
        <CCol class="col-7">
          <CFormInput v-model="nCategory.name" required />
        </CCol>
      </CRow>
      <CRow class="mb-3">
        <CFormLabel for="category-name" class="col-3 col-form-label text-right">
          담당자
        </CFormLabel>
        <CCol class="col-7">
          <CFormSelect v-model="nCategory.assigned_to">
            <option value=""></option>
          </CFormSelect>
        </CCol>
      </CRow>
    </CModalBody>
    <CModalFooter>
      <CButton color="light" @click="closeModal"> 닫기</CButton>
      <CButton type="submit" color="primary">저장</CButton>
    </CModalFooter>
  </CForm>
</template>
