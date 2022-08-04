<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <h1>회원가입</h1>
    <p class="text-muted">Create your account</p>
    <CInputGroup class="mb-3">
      <CInputGroupText>
        <CIcon icon="cil-user" />
      </CInputGroupText>
      <CFormInput
        v-model="username"
        autocomplete="username"
        placeholder="아이디를 입력해주세요"
        required
      />
      <CFormFeedback invalid>아이디를 입력하세요.</CFormFeedback>
    </CInputGroup>

    <CInputGroup class="mb-3">
      <CInputGroupText>@</CInputGroupText>
      <CFormInput
        v-model="email"
        type="email"
        autocomplete="email"
        placeholder="이메일을 입력해주세요"
        required
      />
      <CFormFeedback invalid>이메일을 입력하세요.</CFormFeedback>
    </CInputGroup>

    <CInputGroup class="mb-3">
      <CInputGroupText>
        <CIcon icon="cil-lock-locked" />
      </CInputGroupText>
      <CFormInput
        ref="password"
        v-model="password"
        type="password"
        autocomplete="password"
        placeholder="비밀번호를 입력해주세요"
        required
      />
      <CFormFeedback invalid>비밀번호를 입력하세요.</CFormFeedback>
    </CInputGroup>

    <CInputGroup class="mb-4">
      <CInputGroupText>
        <CIcon icon="cil-lock-locked" />
      </CInputGroupText>
      <CFormInput
        v-model="passwordConfirm"
        type="password"
        autocomplete="password-confirm"
        placeholder="비밀번호를 한번 더 입력해주세요"
        required
      />
      <CFormFeedback invalid>비밀번호를 한번 더 입력하세요.</CFormFeedback>
    </CInputGroup>

    <CRow>
      <CCol>
        <CButton
          type="button"
          color="link"
          class="px-0"
          @click="$router.push({ name: 'Login' })"
        >
          로그인하러 가기
        </CButton>
      </CCol>
    </CRow>

    <div class="d-grid">
      <CButton type="submit" color="primary">회원 가입</CButton>
    </div>
  </CForm>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'RegisterForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      passwordConfirm: '',
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
        const { username, email, password, passwordConfirm } = this
        const staffauth = { company: 1 }
        if (password !== passwordConfirm) {
          alert('비밀번호가 일치하지 않습니다.')
          ;(this as any).$refs.password.$el.focus()
          return
        }
        this.$emit('onSubmit', { username, email, password, staffauth })
        this.validated = false
      }
    },
  },
})
</script>
