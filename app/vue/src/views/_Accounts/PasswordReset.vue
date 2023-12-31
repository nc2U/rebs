<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccount } from '@/store/pinia/account'
import LoginForm from './components/LoginForm.vue'
import FindPassword from '@/views/_Accounts/components/FindPassword.vue'

const formName = ref('login')
const account = useAccount()
const router = useRouter()

const onSubmit = (payload: { email: string; password: string; redirect: string }) => {
  account.login(payload).then(() => {
    if (payload.redirect) router.push({ path: payload.redirect })
    else router.push({ name: 'Home' })
  })
}

const toLogin = () => (formName.value = 'login')
const findPass = () => (formName.value = 'pass')

const passwordReset = (payload: { email: string }) => {
  if (confirm('이메일 전송을 진행하시겠습니까?')) {
    account.resetPassword(payload)
    formName.value = 'login'
  }
}
</script>

<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="8" lg="6" xl="4">
          <CCard class="p-4">
            <CCardBody class="text-body">
              <LoginForm v-if="formName === 'login'" @on-submit="onSubmit" @find-pass="findPass" />

              <FindPassword
                v-else-if="formName === 'pass'"
                @on-submit="passwordReset"
                @to-login="toLogin"
              />
              <CRow>
                <CCol xs="12" class="mt-3">
                  <p class="text-medium-emphasis">Sign with</p>
                </CCol>
                <CCol xs="12">
                  <CIcon icon="cib-google" height="25" class="text-medium-emphasis mr-2"></CIcon>
                  <CIcon icon="cib-github" height="25" class="text-medium-emphasis mr-2"></CIcon>
                  <CIcon icon="cib-facebook" height="25" class="text-medium-emphasis"></CIcon>
                </CCol>
              </CRow>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>
