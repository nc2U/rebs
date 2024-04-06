<script lang="ts" setup>
import { onBeforeMount } from 'vue'
import SearchList from '@/views/_Work/Manages/Projects/components/SearchList.vue'

const emit = defineEmits(['aside-visible'])

onBeforeMount(() => emit('aside-visible', true))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>달력</h5>
    </CCol>
  </CRow>

  <SearchList />

  <CRow class="mb-3">
    <CCol> Calendar!!!</CCol>
  </CRow>

  <CRow>
    <CCol>
      <v-icon icon="mdi-arrow-right-bold" color="success" size="sm" />
      오늘 시작하는 업무(task)
    </CCol>
  </CRow>
  <CRow>
    <CCol>
      <v-icon icon="mdi-arrow-left-bold" color="danger" size="sm" />
      오늘 종료하는 업무(task)
    </CCol>
  </CRow>
  <CRow>
    <CCol>
      <v-icon icon="mdi-rhombus" color="danger" size="sm" />
      오늘 시작하고 종료하는 업무(task)
    </CCol>
  </CRow>
</template>
