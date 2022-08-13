<script lang="ts" setup>
import { useAccount } from '@/store/pinia/account'
import LoginForm from './components/LoginForm.vue'

const account = useAccount()

const onSubmit = (payload: {
  email: string
  password: string
  redirect: string
}) => account.login(payload)
</script>

<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="8" lg="6" xl="4">
          <CCard class="p-4">
            <CCardBody>
              <LoginForm @onSubmit="onSubmit" />
              <CRow>
                <CCol xs="12" class="mt-3">
                  <p class="text-medium-emphasis">Sign with</p>
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
