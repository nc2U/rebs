<template>
  <CForm
    novalidate
    :validated="validated"
    class="needs-validation"
    @submit.prevent="onSubmit"
  >
    <h1>로그인</h1>
    <p class="text-muted">Sign In to your account</p>
    <CInputGroup class="mb-3">
      <CInputGroupText>
        <CIcon icon="cil-user" />
      </CInputGroupText>
      <CFormInput
        v-model="email"
        autoComplete="username email"
        placeholder="이메일주소를 입력해주세요"
        required
      />
      <CFormFeedback invalid>이메일을 입력하세요.</CFormFeedback>
    </CInputGroup>
    <CInputGroup class="mb-4">
      <CInputGroupText>
        <CIcon icon="cil-lock-locked" />
      </CInputGroupText>
      <CFormInput
        type="password"
        v-model="password"
        autoComplete="current-password"
        placeholder="비밀번호를 입력해주세요"
        required
      />
      <CFormFeedback invalid>비밀번호를 입력하세요.</CFormFeedback>
    </CInputGroup>
    <CRow class="text-center">
      <CCol xs="6">
        <CButton type="button" color="link" class="px-0">
          <!--          아이디 | 비밀번호 찾기-->
        </CButton>
      </CCol>
      <CCol xs="6">
        <CButton
          type="button"
          color="link"
          class="px-0"
          @click="$router.push({ name: 'Register' })"
        >
          회원가입하러 가기
        </CButton>
      </CCol>
      <CCol xs="12" class="d-grid">
        <CButton color="primary" class="px-4">로그인</CButton>
      </CCol>
    </CRow>
  </CForm>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'LoginForm',
  data() {
    return {
      email: '',
      password: '',
      redirect: this.$route.query.redirect,
      validated: false,
    }
  },
  methods: {
    onSubmit(event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        this.validated = true
      } else {
        const { email, password, redirect } = this
        this.$emit('onSubmit', { email, password, redirect })
        this.validated = false
      }
    },
  },
})
</script>
