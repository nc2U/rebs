<script lang="ts" setup>
import { ref } from 'vue'
import { isValidate } from '@/utils/helper'
import DatePicker from '@/components/DatePicker/index.vue'

const emit = defineEmits(['close'])

const validated = ref(false)

const nVersion = ref({
  name: '',
  description: '',
  wiki_page_title: '',
  effective_date: null as string | null,
  sharing: '0' as '0' | '1' | '2' | '3' | '4',
  is_default: false,
})

const createVersion = (event: Event) => {
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
  <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="createVersion">
    <CModalBody class="text-body">
      <CRow class="mb-3">
        <CFormLabel for="name" class="col-sm-3 col-form-label text-right required">
          이름
        </CFormLabel>

        <CCol class="col-7">
          <CFormInput v-model="nVersion.name" required />
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="description" class="col-sm-3 col-form-label text-right"> 설명</CFormLabel>

        <CCol class="col-7">
          <CFormInput v-model="nVersion.description" />
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="name" class="col-sm-3 col-form-label text-right"> 위키 페이지</CFormLabel>

        <CCol class="col-7">
          <CFormInput v-model="nVersion.wiki_page_title" />
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="name" class="col-sm-3 col-form-label text-right"> 날짜</CFormLabel>

        <CCol class="col-7">
          <DatePicker v-model="nVersion.effective_date" />
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="name" class="col-sm-3 col-form-label text-right"> 공유</CFormLabel>

        <CCol class="col-7">
          <CFormSelect v-model="nVersion.sharing">
            <option value="0">공유 없음</option>
            <option value="1">하위 프로젝트</option>
            <option value="2">상위 및 하위 프로젝트</option>
            <option value="3">최상위 및 모든 하위 프로젝트</option>
            <option value="4">모든 프로젝트</option>
          </CFormSelect>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="name" class="col-sm-3 col-form-label text-right"> 기본 버전</CFormLabel>

        <CCol class="col-7 pt-2">
          <CFormCheck v-model="nVersion.is_default" />
        </CCol>
      </CRow>
    </CModalBody>

    <CModalFooter>
      <CButton color="light" @click="closeModal">닫기</CButton>
      <CButton type="submit" color="primary">저장</CButton>
    </CModalFooter>
  </CForm>
</template>
