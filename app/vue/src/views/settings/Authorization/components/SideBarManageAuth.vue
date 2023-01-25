<script lang="ts" setup>
import {ref} from 'vue'

const msg = ref('사이드메뉴 관리')
const auths = ['권한없음', {label: '읽기권한', value: '1'}, {label: '쓰기권한', value: '2'}]
const isInActive = true
</script>

<template>
  <Crow>
    <CCol>
      <CRow class="mb-3">
        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-success">
                분양계약 관리
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-primary">
                분양수납 관리
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                고객고지 관리
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                현장자금 관리
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                현장문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                신규 프로젝트
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                본사회계 관리
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                본사문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                본사인사 관리
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                회사관련 설정
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                권한설정 관리
              </CFormLabel>
              <CCol>
                <CFormSelect :options="auths" :disabled="isInActive"/>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <!--            <CFormLabel class="col-md-4 col-form-label">-->
              <!--              분양 계약 관리-->
              <!--            </CFormLabel>-->
              <!--            <CCol>-->
              <!--              <CFormSelect :options="auths"/>-->
              <!--            </CCol>-->
            </CRow>
          </CCol>
        </CRow>
      </CRow>
    </CCol>
  </Crow>
</template>
