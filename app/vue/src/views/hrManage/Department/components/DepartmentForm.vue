<script lang="ts" setup="">
import { ref, computed, onBeforeMount, watch, inject } from 'vue'
import { isValidate } from '@/utils/helper'
import { write_human_resource } from '@/utils/pageAuth'
import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const departs = inject('departs')

const props = defineProps({
  company: {
    type: Number,
    default: null,
  },
  department: {
    type: Object,
    default: null,
  },
})
const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const validated = ref(false)

const form = ref({
  company: null as number | null,
  upper_depart: null,
  name: '',
  task: '',
})

const formsCheck = computed(() => {
  if (props.department) {
    const a = form.value.upper_depart === props.department.obupper_departj
    const b = form.value.name === props.department.name

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

onBeforeMount(() => {
  form.value.company = !!props.company ? props.company : null
  if (props.department) {
    form.value.company = props.department.company
    form.value.upper_depart = props.department.upper_depart
    form.value.name = props.department.name
    form.value.task = props.department.task
  }
})

watch(
  () => props.company,
  newVal => {
    if (!!newVal) form.value.company = newVal
    else form.value.company = null
  },
)
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
              <CFormLabel class="col-sm-4 col-form-label">상위부서</CFormLabel>
              <CCol sm="8">
                <Multiselect
                  v-model.number="form.upper_depart"
                  :options="departs"
                  autocomplete="label"
                  :classes="{ search: 'form-control multiselect-search' }"
                  :add-option-on="['enter' | 'tab']"
                  searchable
                  placeholder="상위부서"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">부서명</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.name"
                  required
                  placeholder="부서명"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
        <CRow>
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">주요업무</CFormLabel>
              <CCol sm="10">
                <CFormTextarea v-model="form.task" placeholder="주요업무" />
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
    <template #header>부서 정보 삭제</template>
    <template #default>
      삭제한 데이터는 복구할 수 없습니다. 해당 정보를 삭제하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
