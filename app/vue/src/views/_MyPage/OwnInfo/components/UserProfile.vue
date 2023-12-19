<script lang="ts" setup>
import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'

defineProps({
  profile: { type: Object, default: null },
})

const accountStore = useAccount()
const userInfo = computed(() => accountStore.userInfo)
</script>

<template>
  <CCardBody class="p-5">
    <CRow class="flex-md-row flex-column-reverse">
      <CCol md="4">
        <CRow class="mb-3">
          <h6>사용자 계정</h6>
          <CFormLabel for="companyCeo" class="col-sm-4 col-form-label"> 아이디</CFormLabel>

          <CCol sm="8">{{ userInfo?.username || '' }}</CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="companyName" class="col-sm-4 col-form-label"> 이메일 주소</CFormLabel>

          <CCol sm="8">{{ userInfo?.email || '' }}</CCol>
        </CRow>

        <v-divider class="my-4" />

        <CRow class="mb-3">
          <h6>사용자 프로필</h6>
          <CFormLabel for="companyName" class="col-sm-4 col-form-label"> 성명</CFormLabel>

          <CCol sm="8">{{ userInfo?.profile?.name || '' }}</CCol>
        </CRow>
        <CRow class="mb-3">
          <CFormLabel for="companyCeo" class="col-sm-4 col-form-label"> 생년월일</CFormLabel>

          <CCol sm="8">{{ userInfo?.profile?.birth_date || '' }}</CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="companyCeo" class="col-sm-4 col-form-label"> 휴대전화</CFormLabel>

          <CCol sm="8">{{ userInfo?.profile?.cell_phone || '' }}</CCol>
        </CRow>
      </CCol>
      <CCol md="8"></CCol>
    </CRow>
  </CCardBody>
</template>
