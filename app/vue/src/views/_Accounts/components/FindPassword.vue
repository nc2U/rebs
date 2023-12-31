<script lang="ts" setup>
import { ref } from 'vue'

const emit = defineEmits(['on-submit', 'to-login'])

const email = ref('')
const validated = ref(false)

const onSubmit = (event: Event) => {
  const el = event.currentTarget as HTMLInputElement
  if (!el.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()

    validated.value = true
  } else {
    emit('on-submit', { email: email.value })
    validated.value = false
  }
}

const toLogin = () => emit('to-login')
</script>

<template>
  <CForm novalidate :validated="validated" class="needs-validation" @submit.prevent="onSubmit">
    <CRow>
      <!--      <CCol><h3>이메일 찾기</h3></CCol>-->
      <CCol><h3>비밀번호 찾기</h3></CCol>
    </CRow>
    <v-divider />
    <p class="text-muted mb-4">
      가입하신 이메일 주소를 입력해 주세요.<br />
      이메일 주소로 비밀번호를 재설정할 수 있는 이메일을 보내드립니다.
    </p>
    <CInputGroup class="mb-3">
      <CInputGroupText>
        <CIcon icon="cil-user" />
      </CInputGroupText>
      <CFormInput
        v-model="email"
        type="email"
        auto-complete="username email"
        placeholder="이메일주소를 입력해주세요"
        required
      />
      <CFormFeedback invalid>가입 시 등록한 이메일을 입력하세요.</CFormFeedback>
    </CInputGroup>

    <CRow>
      <CCol xs="12" class="d-grid">
        <CButton color="danger" class="px-4" size="lg" type="submit">이메일 전송하기</CButton>
      </CCol>
    </CRow>
    <CRow>
      <CCol class="text-right">
        <CButton type="button" color="link" class="px-0" @click="toLogin">
          로그인 화면으로
        </CButton>
      </CCol>
    </CRow>
  </CForm>
</template>
