<script lang="ts" setup>
import { ref } from 'vue'
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>로드맵</h5>
    </CCol>

    <CCol class="text-right">
      <span class="mr-2 form-text">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '(로드맵) - 추가' }" class="ml-1"> 새 버전 </router-link>
      </span>
    </CCol>
  </CRow>
</template>
