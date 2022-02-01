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
                    class="text-medium-emphasis"
                  ></CIcon
                  >&nbsp;
                  <CIcon
                    icon="cib-github"
                    height="25"
                    class="text-medium-emphasis"
                  ></CIcon
                  >&nbsp;
                  <CIcon
                    icon="cib-facebook"
                    height="25"
                    class="text-medium-emphasis"
                  ></CIcon>
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
import { mapActions } from 'vuex'
import LoginForm from './components/LoginForm.vue'

export default defineComponent({
  name: 'Login',
  components: {
    LoginForm,
  },
  methods: {
    onSubmit(payload: { email: string; password: string; redirect: string }) {
      const { email, password, redirect } = payload
      this.login({ email, password }).then(() => {
        if (redirect) this.$router.push({ path: redirect })
        else this.$router.push({ name: 'Home' })
      })
    },
    toRegister() {
      this.$router.push({ name: 'Register' })
    },
    ...mapActions('accounts', ['login']),
  },
})
</script>
