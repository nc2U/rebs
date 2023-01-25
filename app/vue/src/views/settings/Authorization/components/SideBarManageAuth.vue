<script lang="ts" setup>
import { ref, reactive } from 'vue'

const auth = ref({
  contract: null,
  payment: null,
  notice: null,
  project_cash: null,
  project_docs: null,
  project: null,
  company_cash: null,
  company_docs: null,
  human_resource: null,
  company_settings: null,
  auth_manage: null,
})

const auths = reactive([
  '권한없음',
  { label: '읽기권한', value: '1' },
  { label: '쓰기권한', value: '2' },
])

const getColor = (status: '1' | '2' | null) => {
  if (status === '1') return 'yellow-darken-2'
  else if (status === '2') return 'success'
  else return 'blue-grey-lighten-1'
}

const isInActive = true
</script>

<template>
  <Crow>
    <CCol>
      <CRow class="mb-3">
        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.contract)"
                />
                분양계약 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.contract"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.payment)"
                />
                분양수납 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.payment"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.notice)"
                />
                고객고지 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.notice"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.project_cash)"
                />
                현장자금 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.project_cash"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.project_docs)"
                />
                현장문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.project_docs"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.project)"
                />
                신규 프로젝트
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.project"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.company_cash)"
                />
                본사회계 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.company_cash"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.company_docs)"
                />
                본사문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.company_docs"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.human_resource)"
                />
                본사인사 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.human_resource"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.company_settings)"
                />
                회사관련 설정
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.company_settings"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel
                class="col-md-4 col-form-label mb-2 mb-md-1 bg-grey-lighten-3"
              >
                <v-icon
                  icon="mdi mdi-account-arrow-left"
                  :color="getColor(auth.auth_manage)"
                />
                권한설정 관리
              </CFormLabel>
              <CCol>
                <CFormSelect
                  v-model="auth.auth_manage"
                  :options="auths"
                  :disabled="isInActive"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1"></CRow>
          </CCol>
        </CRow>
      </CRow>
    </CCol>
  </Crow>
</template>
