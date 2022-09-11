<script setup lang="ts">
import { reactive, ref } from 'vue'

const emit = defineEmits(['onSubmit'])

const passwordForm = ref()

const form = reactive({
  username: '',
  email: '',
  password: '',
  passwordConfirm: '',
})

const validated = ref(false)

const onSubmit = (event: Event) => {
  const el = event.currentTarget as HTMLInputElement
  if (!el.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()

    validated.value = true
  } else {
    if (form.password !== form.passwordConfirm) {
      alert('비밀번호가 일치하지 않습니다.')
      passwordForm.value.focus()
      return
    }
    emit('onSubmit', { ...form })
    validated.value = false
  }
}
</script>

<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <h1 class="text-body">회원가입</h1>
    <p class="text-muted">Create your account</p>
    <CInputGroup class="mb-3">
      <CInputGroupText>
        <CIcon icon="cil-user" />
      </CInputGroupText>
      <CFormInput
        v-model="form.username"
        autocomplete="username"
        placeholder="아이디를 입력해주세요"
        required
      />
      <CFormFeedback invalid>아이디를 입력하세요.</CFormFeedback>
    </CInputGroup>

    <CInputGroup class="mb-3">
      <CInputGroupText>@</CInputGroupText>
      <CFormInput
        v-model="form.email"
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
        ref="passwordForm"
        v-model="form.password"
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
        v-model="form.passwordConfirm"
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
