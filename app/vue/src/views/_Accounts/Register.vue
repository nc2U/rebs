<script setup lang="ts">
import router from '@/router'
import { useAccount } from '@/store/pinia/account'
import RegisterForm from './components/RegisterForm.vue'

interface SignUser {
  email: string
  username: string
  password: string
}

const accountStore = useAccount()

const onSubmit = (payload: SignUser) => {
  accountStore.signup(payload)
  router.replace({ name: 'Login' })
}
</script>

<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="9" lg="7" xl="5">
          <CCard class="mx-4 p-4">
            <CCardBody class="text-body">
              <RegisterForm @onSubmit="onSubmit" />
              <CRow>
                <CCol xs="12" class="mt-3">
                  <p class="text-medium-emphasis">Sign up using</p>
                </CCol>
                <CCol xs="12">
                  <CIcon
                    icon="cib-google"
                    height="25"
                    class="text-medium-emphasis mr-2"
                  >
                  </CIcon>
                  <CIcon
                    icon="cib-github"
                    height="25"
                    class="text-medium-emphasis mr-2"
                  >
                  </CIcon>
                  <CIcon
                    icon="cib-facebook"
                    height="25"
                    class="text-medium-emphasis"
                  >
                  </CIcon>
                </CCol>
              </CRow>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>
