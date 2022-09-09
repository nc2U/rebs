<script lang="ts" setup>
import { ref, reactive, computed, watch, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { dateFormat } from '@/utils/baseMixins'
import { isValidate } from '@/utils/helper'
import { Site } from '@/store/types/project'
import { write_project } from '@/utils/pageAuth'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  site: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const validated = ref(false)

const form = reactive({
  pk: null as number | null,
  project: null as number | null,
  order: null as number | null,
  district: '',
  lot_number: '',
  site_purpose: '',
  official_area: '',
  returned_area: null as number | null,
  rights_restrictions: '',
  dup_issue_date: null as null | string,
})

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)
const isReturned = computed(() => projectStore.project?.is_returned_area)
const siteStore = useSite()

const formsCheck = computed(() => {
  if (props.site) {
    const a = form.project === props.site.project
    const b = form.order === props.site.order
    const c = form.district === props.site.district
    const d = form.lot_number === props.site.lot_number
    const e = form.site_purpose === props.site.site_purpose
    const f = form.official_area === props.site.official_area
    const g = form.returned_area === props.site.returned_area
    const h = form.rights_restrictions === props.site.rights_restrictions
    const i = form.dup_issue_date === props.site.dup_issue_date

    return a && b && c && d && e && f && g && h && i
  } else return false
})

watch(form, val => {
  if (val.dup_issue_date) form.dup_issue_date = dateFormat(val.dup_issue_date)
})

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    if (write_project) multiSubmit({ ...form })
    else alertModal.value.callModal()
  }
}

const multiSubmit = (payload: Site) => {
  emit('multi-submit', payload)
  emit('close')
}

const deleteObject = () => {
  emit('on-delete', { pk: props.site.pk, project: props.site.project })
  delModal.value.close()
  emit('close')
}

const deleteConfirm = () => {
  if (write_project) delModal.value.callModal()
  else alertModal.value.callModal()
}

onBeforeMount(() => {
  if (props.site) {
    form.pk = props.site.pk
    form.project = props.site.project
    form.order = props.site.order
    form.district = props.site.district
    form.lot_number = props.site.lot_number
    form.site_purpose = props.site.site_purpose
    form.official_area = props.site.official_area
    form.returned_area = props.site.returned_area
    form.rights_restrictions = props.site.rights_restrictions
    form.dup_issue_date = props.site.dup_issue_date
  } else {
    form.project = project.value
    form.order = siteStore.siteCount + 1
  }
})
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
              <CFormLabel class="col-sm-4 col-form-label">등록 번호</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.order"
                  required
                  min="0"
                  type="number"
                  placeholder="등록 번호"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol v-if="!isReturned" sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                등기부 발급일
              </CFormLabel>
              <CCol sm="8">
                <DatePicker
                  v-model="form.dup_issue_date"
                  :required="false"
                  maxlength="10"
                  placeholder="등기부 발급일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">행정 동</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.district"
                  required
                  maxlength="10"
                  placeholder="행정 동"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">지번</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.lot_number"
                  required
                  maxlength="10"
                  placeholder="지번"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                공부상 면적 - m<sup>2</sup>
              </CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.official_area"
                  type="number"
                  required
                  min="0"
                  step="0.0000001"
                  placeholder="공부상 면적"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">지목</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.site_purpose"
                  required
                  maxlength="10"
                  placeholder="지목"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow v-if="isReturned" class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                환지 면적 - m<sup>2</sup>
              </CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.returned_area"
                  type="number"
                  min="0"
                  step="0.0000001"
                  placeholder="환지 면적"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                등기부 발급일
              </CFormLabel>
              <CCol sm="8">
                <DatePicker
                  v-model="form.dup_issue_date"
                  :required="false"
                  maxlength="10"
                  placeholder="등기부 발급일"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">
                주요 권리 제한 사항
              </CFormLabel>
              <CCol sm="10">
                <CFormTextarea
                  v-model="form.rights_restrictions"
                  rows="4"
                  placeholder="주요 권리 제한 사항"
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
          :color="site ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="site"
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
    <template #header>
      <CIcon name="cilWarning" />
      사업 부지 정보 삭제
    </template>
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
