<script setup lang="ts">
import { ref } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'

const emit = defineEmits(['on-submit'])

const refFormModal = ref()

const form = ref({
  username: '',
  email: '',
  password: '',
})

const validated = ref()

const onSubmit = () => emit('on-submit', form.value)

const callModal = () => refFormModal.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <FormModal ref="refFormModal">
    <template #icon>
      <v-icon icon="mdi-account-check" color="success" class="mr-2" />
    </template>
    <template #header>사용자 정보 입력</template>
    <template #default>
      <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="onSubmit">
        <CModalBody class="text-body p-4">
          <CRow class="mb-3">
            <CFormLabel for="username" class="col-sm-3 col-form-label">아이디</CFormLabel>
            <CCol sm="9">
              <CFormInput
                v-model="form.username"
                id="username"
                maxlength="20"
                placeholder="아이디"
                required
              />
            </CCol>
          </CRow>
          <CRow class="mb-3">
            <CFormLabel for="email" class="col-sm-3 col-form-label">이메일</CFormLabel>
            <CCol sm="9">
              <CFormInput
                v-model="form.email"
                id="email"
                type="email"
                maxlength="100"
                placeholder="이메일"
                required
              />
            </CCol>
          </CRow>
          <CRow class="mb-4">
            <CFormLabel for="password" class="col-sm-3 col-form-label">비밀번호</CFormLabel>
            <CCol sm="9">
              <CFormInput
                v-model="form.password"
                id="password"
                type="password"
                maxlength="100"
                placeholder="비밀번호"
                required
              />
            </CCol>
          </CRow>

          <v-divider />

          <CRow>
            <CCol class="mb-3">
              <CFormCheck
                type="checkbox"
                id="inform-mail"
                label="새로 생성한 사용자에게 알림 메일 보내기"
                checked
              />
            </CCol>
          </CRow>

          <CRow>
            <CCol sm="12" class="pl-5 mb-3">
              <CFormCheck
                type="radio"
                id="include-link"
                label="패스워드 재설정 링크 포함"
                checked
              />
            </CCol>
            <CRow>
              <CCol sm="5" class="pl-5 mb-3">
                <span class="pl-4">링크 만료 날짜 : </span>
              </CCol>
              <CCol sm="4">
                <CFormSelect size="sm">
                  <option>24</option>
                </CFormSelect>
              </CCol>
              <CCol>시간</CCol>
            </CRow>
            <CCol sm="12" class="pl-5 mb-3">
              <CFormCheck type="radio" id="include-pass" label="사용자 패스워드 포함" />
            </CCol>
            <CCol sm="12" class="pl-5">
              <CFormCheck type="radio" id="except-all" label="재설정 링크 및 패스워드 모두 제외" />
            </CCol>
          </CRow>
        </CModalBody>
        <CModalFooter>
          <CButton color="light" @click="() => refFormModal.close()"> 닫기</CButton>
          <CButton type="submit" color="primary">확인</CButton>
        </CModalFooter>
      </CForm>
    </template>
  </FormModal>
</template>
