<script lang="ts" setup>
import { ref } from 'vue'

const validated = ref()

const onSubmit = () => alert('submitted! (구현 중!)')
</script>

<template>
  <CCardBody>
    <CRow>
      <CCol class="mt-5"><h5>회원 비밀번호 확인</h5></CCol>
    </CRow>

    <v-divider />

    <CForm
      class="needs-validation px-5"
      novalidate
      :validated="validated"
      @submit.prevent="onSubmit"
    >
      <CRow class="my-4">
        <CFormLabel class="col-sm-2 col-form-label">아이디</CFormLabel>
        <CCol sm="4">admin</CCol>
      </CRow>

      <CRow class="my-3">
        <CFormLabel class="col-sm-2 col-form-label">패스워드</CFormLabel>
        <CCol sm="4">
          <CFormInput
            type="password"
            placeholder="패스워드 입력"
            aria-label="password"
            aria-describedby="password"
            text="외부로부터 회원님의 정보를 안전하게 보호하기 위해 비밀번호를 확인하셔야 합니다."
          />
        </CCol>
      </CRow>
      <CRow class="mb-3">
        <CCol class="col-sm-2"></CCol>
        <CCol sm="4" class="text-right">
          <CButton type="submit" color="warning">비밀번호 확인</CButton>
        </CCol>
      </CRow>
    </CForm>
  </CCardBody>
</template>
