<script lang="ts" setup>
import { onBeforeMount } from 'vue'

const emit = defineEmits(['aside-visible'])

onBeforeMount(() => emit('aside-visible', false))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>위키(Wiki)</h5>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CFormTextarea></CFormTextarea>
    </CCol>
  </CRow>

  <CRow class="mt-2">
    <CCol>
      <CButton color="primary">저장</CButton>
      <CButton color="light">취소</CButton>
    </CCol>
  </CRow>
</template>
