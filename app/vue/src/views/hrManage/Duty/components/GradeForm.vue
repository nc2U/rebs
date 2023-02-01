<script lang="ts" setup="">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { isValidate } from '@/utils/helper'
import { write_human_resource } from '@/utils/pageAuth'
import { Grade } from '@/store/types/company'
// import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  company: {
    type: String,
    default: null,
  },
  grade: {
    type: Object,
    default: null,
  },
})
const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const validated = ref(false)

const form = ref<Grade>({
  pk: undefined,
  company: undefined,
  grade: '',
  promotion_period: '',
  criteria_new: '',
})

const formsCheck = computed(() => {
  if (props.grade) {
    const a = form.value.grade === props.grade.grade
    const b = form.value.promotion_period === props.grade.promotion_period
    const c = form.value.criteria_new === props.grade.criteria_new

    return a && b && c
  } else return false
})

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    if (write_human_resource.value) multiSubmit({ ...form.value })
    else alertModal.value.callModal()
  }
}

const multiSubmit = (payload: Grade) => {
  emit('multi-submit', payload)
  emit('close')
}

const deleteObject = (pk: number) => {
  emit('on-delete', pk)
  delModal.value.close()
  emit('close')
}

const deleteConfirm = () => {
  if (write_human_resource.value) delModal.value.callModal()
  else alertModal.value.callModal()
}

onBeforeMount(() => {
  if (props.grade) {
    form.value.pk = props.grade.pk
    form.value.company = props.grade.company
    form.value.grade = props.grade.grade
    form.value.promotion_period = props.grade.promotion_period
    form.value.criteria_new = props.grade.criteria_new
  } else form.value.company = props.company
})

watch(
  () => props.company,
  newVal => {
    if (!!newVal) form.value.company = newVal
    else form.value.company = undefined
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
        <CRow class="mb-3"></CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">등급</CFormLabel>
              <CCol sm="8">
                <CFormInput v-model="form.grade" required placeholder="등급" />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                승급표준년수
              </CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.promotion_period"
                  type="number"
                  placeholder="승급표준년수"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">
                신입부여기준
              </CFormLabel>
              <CCol sm="10">
                <CFormInput
                  v-model="form.criteria_new"
                  placeholder="신입부여기준"
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
          :color="grade ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="grade"
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
    <template #header>직급 정보 삭제</template>
    <template #default>
      삭제한 데이터는 복구할 수 없습니다. 해당 정보를 삭제하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="deleteObject(grade.pk)">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
