<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { hashCode } from '@/utils/helper'
import AlertModal from '@/components/Modals/AlertModal.vue'

const alertModal = ref()

const registerCode = ref('')
const validated = ref(false)

const store = useStore()
const router = useRouter()

const onSubmit = (event: Event) => {
  const form = event.currentTarget as HTMLInputElement
  if (!form.checkValidity()) {
    event.preventDefault()
    event.stopPropagation()

    validated.value = true
  } else {
    if (registerCode.value === store.state.registerCode) {
      router.push({
        name: 'Register',
        query: { id: hashCode(registerCode.value).toString() },
      })
    } else
      alertModal.value.callModal(
        '계정 생성코드 오류',
        '계정 생성코드가 맞지 않습니다. 계정 생성코드를 확인 후 다시 시도하여\n' +
          '          주십시요.',
      )
  }
}
</script>

<template>
  <div class="bg-light min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="8" lg="6" xl="4">
          <CCard class="p-4 text-body">
            <CCardBody>
              <CRow class="mb-3">
                <h2>계정 생성코드 입력</h2>
              </CRow>
              <CRow>
                <CCol>
                  <p class="text-medium-emphasis">
                    이 사이트는 (주)바램디앤씨의 업무관리 시스템입니다.
                  </p>
                  <p class="text-medium-emphasis">
                    계정 등록을 위하여 <u>계정 생성코드</u>가 필요합니다.
                  </p>
                </CCol>
              </CRow>

              <CForm
                class="needs-validation"
                :validated="validated"
                novalidate
                @submit.prevent="onSubmit"
              >
                <CRow class="mb-2">
                  <CCol>
                    <CFormInput
                      v-model="registerCode"
                      type="password"
                      required
                    />
                  </CCol>
                </CRow>
                <CRow>
                  <CCol class="d-grid gap-2 mb-2">
                    <CButton class="btn btn-primary" type="submit">
                      제출하기
                    </CButton>
                  </CCol>
                </CRow>
              </CForm>

              <CRow>
                <CCol xs="12">
                  <p class="text-medium-emphasis">
                    계정 생성코드 발급 및 가입 후 시스템 이용 관련 권한 관련
                    사항은 관리자에게 문의하여 주시기 바랍니다.
                  </p>
                </CCol>
              </CRow>

              <CRow>
                <CCol>
                  <p>
                    <router-link :to="{ name: 'Login' }">
                      로그인 화면으로 돌아가기
                    </router-link>
                  </p>
                </CCol>
              </CRow>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>

      <AlertModal ref="alertModal" />
    </CContainer>
  </div>
</template>
