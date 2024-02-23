<script lang="ts" setup="">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <CRow>
    <CCol>{{ route.name }}</CCol>
  </CRow>
</template>
