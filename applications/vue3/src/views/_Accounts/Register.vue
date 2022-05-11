<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="9" lg="7" xl="5">
          <CCard class="mx-4">
            <CCardBody class="p-4">
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

<script lang="ts">
import { defineComponent } from 'vue'
import RegisterForm from './components/RegisterForm.vue'
import { mapActions } from 'vuex'

export default defineComponent({
  name: 'Register',
  components: { RegisterForm },
  methods: {
    onSubmit(payload: {
      email: string
      username: string
      password: string
      staffauth: any
    }) {
      this.signup(payload)
    },
    ...mapActions('accounts', ['signup']),
  },
})
</script>
