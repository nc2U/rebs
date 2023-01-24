<script lang="ts" setup>
import { ref } from 'vue'

const msg = ref('사이드메뉴 관리')
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
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-primary">
                분양수납 관리
              </CFormLabel>
              <CCol>
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                고객고지 관리
              </CFormLabel>
              <CCol>
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
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
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                현장문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                신규 프로젝트
              </CFormLabel>
              <CCol>
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
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
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                본사문서 관리
              </CFormLabel>
              <CCol>
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                본사인사 관리
              </CFormLabel>
              <CCol>
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
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
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <CFormLabel class="col-md-4 col-form-label bg-light">
                권한설정 관리
              </CFormLabel>
              <CCol>
                <CFormSelect>
                  <option value="0">권한없음</option>
                  <option value="1">읽기권한</option>
                  <option value="2">쓰기권한</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
          <CCol md="4">
            <CRow class="m-1">
              <!--            <CFormLabel class="col-md-4 col-form-label">-->
              <!--              분양 계약 관리-->
              <!--            </CFormLabel>-->
              <!--            <CCol>-->
              <!--              <CFormSelect>-->
              <!--                <option value="0">권한없음</option>-->
              <!--                <option value="1">읽기권한</option>-->
              <!--                <option value="2">쓰기권한</option>-->
              <!--              </CFormSelect>-->
              <!--            </CCol>-->
            </CRow>
          </CCol>
        </CRow>
      </CRow>
    </CCol>
  </Crow>
</template>
