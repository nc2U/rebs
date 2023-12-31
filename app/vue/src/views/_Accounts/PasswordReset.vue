<script lang="ts" setup>
import { useRoute, useRouter } from 'vue-router'
import ResetForm from '@/views/_Accounts/components/ResetForm.vue'
import SocialLogin from '@/views/_Accounts/components/SocialLogin.vue'
import { useAccount } from '@/store/pinia/account'

const accStore = useAccount()
const [route, router] = [useRoute(), useRouter()]

const onSubmit = async (new_password: string) => {
  const payload = {
    user_id: route.query.uidb64,
    token: route.query.token,
    new_password,
  }
  console.log(payload)
  accStore.passResetConfirm(payload)

  await router.push({ name: 'Home' })
}
</script>

<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="8" lg="6" xl="4">
          <CCard class="p-4">
            <CCardBody class="text-body">
              <ResetForm @on-submit="onSubmit" />

              <SocialLogin />

              {{ route.query }}
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>
