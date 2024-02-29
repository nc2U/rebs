<script lang="ts" setup>
import { computed } from 'vue'
import { useWork } from '@/store/pinia/work'

const workStore = useWork()
const iProject = computed(() => workStore.issueProject)
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>개요</h5>
    </CCol>
  </CRow>

  <CRow>
    <CCol>{{ iProject }}</CCol>
  </CRow>
</template>
