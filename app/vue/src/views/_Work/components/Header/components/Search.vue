<script lang="ts" setup="">
import { ref } from 'vue'
import Option from '@/views/projects/Option/components/Option.vue'

const msg = ref('head search')
</script>

<template>
  <CRow>
    <CCol class="p-1">
      <CInputGroup size="" class="mb-3">
        <CInputGroupText id="inputGroup-sizing-sm">검색</CInputGroupText>
        <CFormInput aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" />
      </CInputGroup>
    </CCol>
    <CCol class="p-1">
      <CFormSelect size="" class="mb-3">
        <option>프로젝트 바로가기</option>
      </CFormSelect>
    </CCol>
  </CRow>
</template>
