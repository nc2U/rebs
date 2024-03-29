<script lang="ts" setup>
import { computed } from 'vue'
import NoData from '@/views/_Work/components/NoData.vue'

const iCategoryList = computed(() => [])
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="mr-2 form-text">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link to="" class="ml-1">새 업무범주</router-link>
      </span>
    </CCol>
  </CRow>

  <NoData v-if="!iCategoryList.length" />

  <CRow v-else>
    <CCol></CCol>
  </CRow>
</template>
