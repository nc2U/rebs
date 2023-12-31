<script lang="ts" setup>
import { ref, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ResetForm from '@/views/_Accounts/components/ResetForm.vue'
import SocialLogin from '@/views/_Accounts/components/SocialLogin.vue'

const uidb64 = ref('')
const token = ref('')

const [route, router] = [useRoute(), useRouter()]

const onSubmit = (password: string) => {
  console.log(password)
  alert(password)

  router.push({ name: 'Login' })
}

onBeforeMount(() => {
  if (route.query.uidb64) uidb64.value = route.query.uidb64 as string
  if (route.query.token) token.value = route.query.token as string
})
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
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>
