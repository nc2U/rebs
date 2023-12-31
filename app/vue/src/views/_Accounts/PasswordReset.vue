<script lang="ts" setup>
import { useRouter } from 'vue-router'
import { useAccount } from '@/store/pinia/account'
import ResetForm from '@/views/_Accounts/components/ResetForm.vue'
import SocialLogin from '@/views/_Accounts/components/SocialLogin.vue'

const account = useAccount()
const router = useRouter()

const onSubmit = (payload: { email: string; password: string; redirect: string }) => {
  account.login(payload).then(() => {
    if (payload.redirect) router.push({ path: payload.redirect })
    else router.push({ name: 'Home' })
  })
}

const passwordReset = (payload: { email: string }) => {
  if (confirm('이메일 전송을 진행하시겠습니까?')) {
    account.resetPassword(payload)
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
              <ResetForm @on-submit="passwordReset" />

              <SocialLogin />
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>
