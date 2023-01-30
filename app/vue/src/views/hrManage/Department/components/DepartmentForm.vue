<script lang="ts" setup="">
import { ref, reactive, computed } from 'vue'
import { isValidate } from '@/utils/helper'
import { write_human_resource } from '@/utils/pageAuth'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  department: {
    type: Object,
    default: null,
  },
})
const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const validated = ref(false)

const form = reactive({
  obj1: null,
  obj2: null,
})

const formsCheck = computed(() => {
  if (props.department) {
    const a = form.obj1 === props.department.obj1
    const b = form.obj2 === props.department.obj2

    return a && b
  } else return false
})

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    if (write_human_resource.value) multiSubmit({ ...form })
    else alertModal.value.callModal()
  }
}

const multiSubmit = (payload: any) => {
  emit('multi-submit', payload)
  emit('close')
}

const deleteObject = () => {
  emit('on-delete', {})
  delModal.value.close()
  emit('close')
}

const deleteConfirm = () => {
  if (write_human_resource.value) delModal.value.callModal()
  else alertModal.value.callModal()
}
</script>

<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CModalBody class="p-4">
      <div>
        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">항목이름1</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.obj1"
                  required
                  placeholder="항목이름1"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">항목이름2</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.obj2"
                  required
                  placeholder="항목이름2"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </div>
    </CModalBody>

    <CModalFooter>
      <CButton type="button" color="light" @click="$emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          type="submit"
          :color="department ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="department"
          type="button"
          color="danger"
          @click="deleteConfirm"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>
  </CForm>

  <ConfirmModal ref="delModal">
    <template #header>사업 부지 정보 삭제</template>
    <template #default>
      삭제한 데이터는 복구할 수 없습니다. 해당 사업 부지 정보를
      삭제하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
