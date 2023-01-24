<script lang="ts" setup>
import { ref } from 'vue'

const msg = ref('프로젝트 관리')
</script>

<template>
  <CCallout color="secondary" class="mb-4">
    <CRow>
      <CCol md="4">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label">
            허용 프로젝트
          </CFormLabel>
          <CCol>
            <CFormSelect disabled>
              <option value="0">프로젝트1</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol md="4">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label">
            담당 메인 프로젝트
          </CFormLabel>
          <CCol>
            <CFormSelect disabled>
              <option value="0">프로젝트1</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
  <hr />
</template>
