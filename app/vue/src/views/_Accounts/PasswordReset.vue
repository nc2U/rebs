<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ResetForm from '@/views/_Accounts/components/ResetForm.vue'
import SocialLogin from '@/views/_Accounts/components/SocialLogin.vue'
import { useAccount } from '@/store/pinia/account'

const accStore = useAccount()
const [route, router] = [useRoute(), useRouter()]

const uid = computed(() => Number(atob(route.query.uidb64 as string)))
const token = computed(() => route.query.token)
const isExpired = computed(() => {
  const resetToken = accStore.resetTokenList.length ? accStore.resetTokenList[0] : null
  if (!!resetToken) {
    if (resetToken.is_expired) return true // expired!
    else return token.value !== resetToken.token // if tokenCheck true -> not expired!, false -> expired!
  } else return true
})

const fetchResetTokenList = (user: number) => accStore.fetchResetTokenList(user)

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

onBeforeMount(() => fetchResetTokenList(uid.value))
</script>

<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="8" lg="6" xl="4">
          <CCard class="p-4">
            <CCardBody v-if="isExpired" class="text-center text-danger">
              <h2>This Token was Expired!</h2>
              <div class="text-left pt-3">
                <p class="text-muted">
                  이 토큰의 비밀번호 재설정 가능시간이 만료되었습니다. 비밀번호를 재설정 하려면 다시
                  요청해 주십시요.
                </p>
              </div>
              <div class="text-right pt-2">
                <router-link :to="{ name: 'Login' }">To Login</router-link>
              </div>
            </CCardBody>
            <CCardBody v-else class="text-body">
              <ResetForm @on-submit="onSubmit" />

              <SocialLogin />
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>
