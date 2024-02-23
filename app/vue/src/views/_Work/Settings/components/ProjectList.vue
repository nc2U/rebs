<script lang="ts" setup="">
import { ref } from 'vue'
</script>

<template>
  <CRow>
    <CCol>
      <h6>{{ $route.name || '프로젝트' }}</h6>
    </CCol>
    <CCol class="text-right">
      <router-link :to="{ name: '프로젝트 - 생성' }">새 프로젝트</router-link>
      <router-link :to="{ name: '프로젝트 목록' }" class="ml-3">관리</router-link>
    </CCol>
  </CRow>

  <!--  <router-link :to="{ name: '(개요)', params: { projId: 'dongchun' } }">-->
  <!--    개별 프로젝트-->
  <!--  </router-link>-->
</template>
