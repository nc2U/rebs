<script lang="ts" setup="">
import { computed } from 'vue'
import NoData from '@/views/_Work/components/NoData.vue'

const memberList = computed(() => [])
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link to="" class="ml-1">새 구성원</router-link>
      </span>
    </CCol>

    <CCol class="text-right">
      <span>
        <v-icon icon="mdi-cog" color="secondary" size="sm" />
        <router-link to="" class="ml-1">관리</router-link>
      </span>
    </CCol>
  </CRow>

  <NoData v-if="!memberList.length" />

  <CRow v-else>
    <CCol></CCol>
  </CRow>
</template>
