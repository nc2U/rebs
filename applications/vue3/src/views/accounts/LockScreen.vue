<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="6" lg="5" xl="4">
          <CCard class="p-4">
            <CCardBody v-if="lockedUser">
              <CRow class="mb-3 justify-content-center">
                <CAvatar
                  color="secondary"
                  text-color="white"
                  size="xl"
                  status="success"
                >
                  {{ lockedUser.username.toUpperCase().substring(0, 1) }}
                </CAvatar>
              </CRow>
              <CRow>
                <CCol class="text-center mb-4">
                  <h1 class="text-medium-emphasis">
                    {{ lockedUser.username.toUpperCase() }}
                  </h1>
                </CCol>
              </CRow>
              <CRow class="mb-2">
                <CCol>
                  <CForm novalidate>
                    <CInputGroup class="mb-3">
                      <CFormInput
                        type="password"
                        autoComplete="username email"
                        v-model="password"
                        @keypress.enter="toHome"
                        required
                      />
                      <CInputGroupText @click="toHome">
                        <CIcon icon="cilArrowCircleRight"></CIcon>
                      </CInputGroupText>
                    </CInputGroup>
                  </CForm>
                </CCol>
              </CRow>
              <CRow>
                <CCol class="text-center">
                  <p class="text-medium-emphasis">임시 비밀번호 : 0000</p>
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
import { mapActions, mapState } from 'vuex'
import store from '@/store'

export default defineComponent({
  name: 'LockScreen',
  data() {
    return {
      password: '',
    }
  },
  computed: {
    ...mapState('accounts', ['lockedUser']),
  },
  mounted() {
    if (!this.lockedUser) {
      this.$router.push({ name: 'Login' })
    }
  },
  async beforeRouteLeave(to, from, next) {
    if (
      !this.password ||
      this.password !== '0000' ||
      to.name !== '메인 페이지'
    ) {
      next({ name: 'LockScreen' })
    } else {
      next()
    }
  },
  methods: {
    toHome() {
      this.$router.push({ name: '메인 페이지' })
    },
    ...mapActions('accounts', ['login', 'logout']),
  },
})
</script>

<style lang="scss" scoped></style>
