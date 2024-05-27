<script lang="ts" setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { isValidate } from '@/utils/helper'
import { colorLight } from '@/utils/cssMixins'
import DatePicker from '@/components/DatePicker/index.vue'

const emit = defineEmits(['on-submit'])

const validated = ref(false)

const form = ref({
  pk: null as number | null,
  project: null,
  name: '',
  description: '',
  wiki_page_title: '',
  due_date: null as string | null,
  sharing: '0' as '0' | '1' | '2' | '3' | '4',
  isDefault: false,
})

const route = useRoute()
const onSubmit = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    const is_back = !!route.query.back
    emit('on-submit', { ...form.value }, is_back)
  }
}
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>새 버전</h5>
    </CCol>

    <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="onSubmit">
      <CCard :color="colorLight" class="mb-2">
        <CCardBody>
          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right required">
              이름
            </CFormLabel>

            <CCol sm="10" lg="6">
              <CFormInput v-model="form.name" required />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right"> 설명</CFormLabel>

            <CCol sm="10" lg="6">
              <CFormInput v-model="form.description" />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right">
              위키 페이지
            </CFormLabel>

            <CCol sm="10" lg="6">
              <CFormInput v-model="form.wiki_page_title" />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right"> 날짜</CFormLabel>

            <CCol sm="6">
              <DatePicker v-model="form.due_date" />
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right"> 공유</CFormLabel>

            <CCol sm="6">
              <CFormSelect v-model="form.sharing">
                <option value="0">공유 없음</option>
                <option value="1">하위 프로젝트</option>
                <option value="2">상위 및 하위 프로젝트</option>
                <option value="3">최상위 및 모든 하위 프로젝트</option>
                <option value="4">모든 프로젝트</option>
              </CFormSelect>
            </CCol>
          </CRow>

          <CRow class="mb-3">
            <CFormLabel for="name" class="col-sm-2 col-form-label text-right">
              기본 버전
            </CFormLabel>

            <CCol sm="6" class="pt-2">
              <CFormCheck v-model="form.isDefault" />
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>

      <CButton type="submit" color="primary"> 저장</CButton>
    </CForm>
  </CRow>
</template>
