<script lang="ts" setup="">
import { ref } from 'vue'

const msg = ref('유저 셀렉트')
</script>

<template>
  <CCallout color="info">
    <CRow>
      <CCol md="4">
        <CRow class="m-1">
          <CFormLabel class="col-md-4 col-form-label"> 사용자 선택</CFormLabel>
          <CCol>
            <CFormSelect>
              <option value="0">---------</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
</template>
