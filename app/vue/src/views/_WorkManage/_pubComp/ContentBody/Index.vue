<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from '@/store'

const isDark = computed(() => useStore().theme === 'dark')
const backGround = computed(() => (isDark.value ? 'bg-dark' : 'bg-white'))
</script>

<template>
  <CRow class="flex-grow-1">
    <CCol md="9" class="text-body pl-4 p-3 main" :class="backGround">a</CCol>
    <CCol class="text-body p-3">b</CCol>
  </CRow>
</template>

<style lang="scss" scoped>
.main {
  border-right: 1px solid #ddd !important;
}

.dark-theme .main {
  border-right: 1px solid #333 !important;
}
</style>
