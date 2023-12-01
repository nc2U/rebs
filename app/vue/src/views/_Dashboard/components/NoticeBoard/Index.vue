<script lang="ts" setup>
import { ref } from 'vue'

const msg = ref('Full list!')
</script>

<template>
  <CContainer fluid>
    <CRow>
      <CCol xl="11" xxl="10">
        {{ msg }}
      </CCol>
    </CRow>
  </CContainer>
</template>
