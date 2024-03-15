<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import NoData from '@/views/_Work/components/NoData.vue'

const emit = defineEmits(['aside-visible'])

const activities = computed(() => [])

onBeforeMount(() => emit('aside-visible', true))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>작업내역</h5>
    </CCol>
  </CRow>

  <CRow class="fst-italic">
    <CCol>2024/02/21부터 2024/03/01까지</CCol>
  </CRow>

  <NoData v-if="!activities.length" />

  <CRow v-else>
    <CCol></CCol>
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
