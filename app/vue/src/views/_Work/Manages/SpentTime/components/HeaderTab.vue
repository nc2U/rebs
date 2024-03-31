<script lang="ts" setup>
import { ref } from 'vue'

const menu = ref('detail')
</script>

<template>
  <CRow class="my-3 pt-2">
    <CCol>
      <v-tabs v-model="menu" density="compact">
        <v-tab value="detail" variant="tonal">자세히</v-tab>
        <v-tab value="report" variant="tonal">보고서</v-tab>
      </v-tabs>
    </CCol>
  </CRow>
</template>
