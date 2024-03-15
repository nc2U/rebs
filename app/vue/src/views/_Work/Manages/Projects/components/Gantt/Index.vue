<script lang="ts" setup>
import { onBeforeMount } from 'vue'
import SearchList from '@/views/_Work/components/SearchList.vue'

const emit = defineEmits(['aside-visible'])

onBeforeMount(() => emit('aside-visible', true))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>Gantt 차트</h5>
    </CCol>
  </CRow>

  <SearchList />

  <CRow class="mb-3">
    <CCol> Gantt Chart</CCol>
  </CRow>

  <CRow>
    <CCol>
      <CButtonGroup role="group">
        <CButton color="primary" variant="outline" size="sm">« 뒤로</CButton>
        <CButton color="primary" variant="outline" size="sm">다음 »</CButton>
      </CButtonGroup>
    </CCol>
  </CRow>
</template>
