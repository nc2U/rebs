<script lang="ts" setup="">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { isValidate } from '@/utils/helper'
import { write_human_resource } from '@/utils/pageAuth'
import { Rank } from '@/store/types/company'
import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  company: {
    type: String,
    default: null,
  },
  rank: {
    type: Object,
    default: null,
  },
})
const emit = defineEmits(['multi-submit', 'on-delete', 'close'])

const delModal = ref()
const alertModal = ref()

const validated = ref(false)

const form = ref<Rank>({
  pk: undefined,
  company: undefined,
  sort: '1',
  level: null,
  rank: '',
  title: '',
  description: '',
})

const formsCheck = computed(() => {
  if (props.rank) {
    const a = form.value.sort === props.rank.sort
    const b = form.value.level === props.rank.level
    const c = form.value.rank === props.rank.rank
    const d = form.value.title === props.rank.title
    const e = form.value.description === props.rank.description

    return a && b && c && d && e
  } else return false
})

const sorts = [
  { value: '1', label: '임원' },
  { value: '2', label: '직원' },
]

const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    if (write_human_resource.value) multiSubmit({ ...form.value })
    else alertModal.value.callModal()
  }
}

const multiSubmit = (payload: Rank) => {
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
  if (props.rank) {
    form.value.pk = props.rank.pk
    form.value.company = props.rank.company
    form.value.sort = props.rank.sort
    form.value.level = props.rank.level
    form.value.rank = props.rank.rank
    form.value.title = props.rank.title
    form.value.description = props.rank.description
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
              <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
              <CCol sm="8">
                <Multiselect
                  v-model="form.sort"
                  :options="sorts"
                  autocomplete="label"
                  :classes="{ search: 'form-control multiselect-search' }"
                  :add-option-on="['enter' | 'tab']"
                  searchable
                  placeholder="구분"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">직급</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.level"
                  required
                  placeholder="직급"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">직책</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.rank"
                  required
                  placeholder="직책"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">직함</CFormLabel>
              <CCol sm="8">
                <CFormInput v-model.number="form.title" placeholder="직함" />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
              <CCol sm="10">
                <CFormTextarea
                  v-model.number="form.description"
                  placeholder="비고"
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
          :color="rank ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="rank"
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
      <CButton color="danger" @click="deleteObject(rank.pk)">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>
