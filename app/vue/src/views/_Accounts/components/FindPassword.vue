<script lang="ts" setup>
import { ref } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const emit = defineEmits(['on-submit', 'to-login'])

const confModal = ref()
const email = ref('')
const validated = ref(false)

const onSubmit = (event: Event) => {
  const el = event.currentTarget as HTMLInputElement
  if (!el.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()

    validated.value = true
  } else {
    confModal.value.callModal()
    validated.value = false
  }
}

const modalAction = () => emit('on-submit', { email: email.value })

const toLogin = () => emit('to-login')
</script>

<template>
  <CForm novalidate :validated="validated" class="needs-validation" @submit.prevent="onSubmit">
    <CRow>
      <!--      <CCol><h3>이메일 찾기</h3></CCol>-->
      <CCol><h3>비밀번호 찾기</h3></CCol>
    </CRow>
    <v-divider />
    <p class="text-muted">
      가입하신 이메일 주소를 입력해 주세요.<br />
      이메일 주소로 비밀번호를 재설정할 수 있는 이메일을 보내드립니다.
    </p>
    <p class="text-muted mb-4">발송된 이메일의 비밀번호 재설정은 10분 간 유효합니다.</p>
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

  <ConfirmModal ref="confModal">
    <template #header>비밀번호 재설정 확인</template>
    <template #default> 비밀번호 재설정을 위한 이메일을 전송하시겠습니까?</template>
    <template #footer>
      <CButton color="danger" @click="modalAction"> 확인</CButton>
    </template>
  </ConfirmModal>
</template>
