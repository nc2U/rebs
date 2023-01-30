<script lang="ts" setup="">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { isValidate } from '@/utils/helper'
import { write_human_resource } from '@/utils/pageAuth'
import { Staff } from '@/store/types/company'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  company: {
    type: String,
    default: null,
  },
  staff: {
    type: Object,
    default: null,
  },
})
const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const validated = ref(false)

const form = ref<Staff>({
  pk: undefined,
  company: undefined,
  department: undefined,
  rank: undefined,
  name: '',
  birth_date: null,
  gender: 'M',
  entered_date: null,
  personal_phone: '',
  email: '',
  status: '1',
})

const formsCheck = computed(() => {
  if (props.staff) {
    const a = form.value.pk === props.staff.pk
    const b = form.value.department === props.staff.department
    const c = form.value.rank === props.staff.rank
    const d = form.value.name === props.staff.name
    const e = form.value.birth_date === props.staff.birth_date
    const f = form.value.gender === props.staff.gender
    const g = form.value.entered_date === props.staff.entered_date
    const h = form.value.personal_phone === props.staff.personal_phone
    const i = form.value.email === props.staff.email
    const j = form.value.status === props.staff.status

    return a && b && c && d && e && f && g && h && i && j
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

const multiSubmit = (payload: Staff) => {
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
  if (props.staff) {
    form.value.pk = props.staff.pk
    form.value.company = props.staff.company
    form.value.department = props.staff.department
    form.value.rank = props.staff.rank
    form.value.name = props.staff.name
    form.value.birth_date = props.staff.birth_date
    form.value.gender = props.staff.gender
    form.value.entered_date = props.staff.entered_date
    form.value.personal_phone = props.staff.personal_phone
    form.value.email = props.staff.email
    form.value.status = props.staff.status
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
        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">성명</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.name"
                  required
                  placeholder="성명"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">성별</CFormLabel>
              <CCol sm="8">
                <CFormInput v-model="form.gender" required placeholder="성별" />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">휴대전화</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.personal_phone"
                  required
                  placeholder="휴대전화"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">이메일</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.email"
                  required
                  placeholder="이메일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">생년월일</CFormLabel>
              <CCol sm="8">
                <CFormInput v-model="form.birth_date" placeholder="생년월일" />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">입사일</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.entered_date"
                  required
                  placeholder="입사일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <hr />

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">부서</CFormLabel>
              <CCol sm="8">
                <CFormInput v-model="form.department" placeholder="부서" />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">직책</CFormLabel>
              <CCol sm="8">
                <CFormInput v-model="form.rank" placeholder="직책" />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">상태</CFormLabel>
              <CCol sm="8">
                <CFormInput v-model="form.status" required placeholder="상태" />
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
          :color="staff ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="staff"
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
    <template #header>직원 정보 삭제</template>
    <template #default>
      삭제한 데이터는 복구할 수 없습니다. 해당 정보를 삭제하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
