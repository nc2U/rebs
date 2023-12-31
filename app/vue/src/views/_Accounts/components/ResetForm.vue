<script lang="ts" setup>
import { ref } from 'vue'

const emit = defineEmits(['on-submit'])

const form = ref({
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
    emit('on-submit', form.value)
    validated.value = false
  }
}
</script>

<template>
  <CForm novalidate :validated="validated" class="needs-validation" @submit.prevent="onSubmit">
    <CRow>
      <!--      <CCol><h3>이메일 찾기</h3></CCol>-->
      <CCol><h3>비밀번호 재설정</h3></CCol>
    </CRow>

    <v-divider />

    <p class="text-muted mb-4">새로운 비밀번호를 입력해 주세요.</p>

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
        placeholder="비밀번호 확인"
        required
      />
      <CFormFeedback invalid>비밀번호를 한번 더 입력하세요.</CFormFeedback>
    </CInputGroup>

    <CRow>
      <CCol xs="12" class="d-grid">
        <CButton color="danger" class="px-4" size="lg" type="submit">비밀번호 재설정하기</CButton>
      </CCol>
    </CRow>
    <CRow>
      <CCol class="text-right">
        <CButton
          type="button"
          color="link"
          class="px-0"
          @click="$router.replace({ name: 'Login' })"
        >
          로그인 화면으로
        </CButton>
      </CCol>
    </CRow>
  </CForm>
</template>
