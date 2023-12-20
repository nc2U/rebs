<script lang="ts" setup>
import { ref } from 'vue'

defineProps({ username: { type: String, default: '' } })
const emit = defineEmits(['check-password'])

const validated = ref(false)
const password = ref('')

const onSubmit = (event: Event) => {
  const e = event.currentTarget as HTMLInputElement
  if (!e.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()

    validated.value = true
  } else emit('check-password', password.value)
}
</script>

<template>
  <CCardBody class="p-5">
    <CRow>
      <CCol><h5>회원 비밀번호 확인</h5></CCol>
    </CRow>

    <v-divider />

    <CForm
      class="needs-validation px-5"
      novalidate
      :validated="validated"
      @submit.prevent="onSubmit"
    >
      <CRow class="pt-3 mb-3">
        <CFormLabel class="col-sm-2 col-lg-1 col-form-label">아이디</CFormLabel>
        <CCol sm="6" lg="4" xl="3" class="pt-2">{{ username }}</CCol>
      </CRow>

      <CRow class="my-3">
        <CFormLabel class="col-sm-2 col-lg-1 col-form-label">패스워드</CFormLabel>
        <CCol sm="6" lg="4" xl="3">
          <CFormInput
            v-model="password"
            type="password"
            required
            placeholder="패스워드 입력"
            aria-label="password"
            aria-describedby="password"
            text="외부로부터 회원님의 정보를 안전하게 보호하기 위해 비밀번호를 확인하셔야 합니다."
          />
        </CCol>
      </CRow>
      <CRow class="mb-3">
        <CCol class="col-sm-2 col-lg-1"></CCol>
        <CCol sm="6" lg="4" xl="3" class="text-right">
          <CButton type="submit" color="info">비밀번호 확인</CButton>
        </CCol>
      </CRow>
    </CForm>
  </CCardBody>
</template>
