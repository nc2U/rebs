<script lang="ts" setup="">
import { computed } from 'vue'
import NoData from '@/views/_Work/components/NoData.vue'

const repoList = computed(() => [])
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link to="" class="ml-1">저장소 추가</router-link>
      </span>
    </CCol>
  </CRow>

  <NoData v-if="!repoList.length" />

  <CRow v-else>
    <CCol></CCol>
  </CRow>
</template>
