<script lang="ts" setup=""></script>

<template>
  <CRow>
    <CCol>
      <h6>새 프로젝트</h6>
    </CCol>

    <CCol class="text-right">
      <span v-show="$route.name !== '프로젝트 - 생성'" class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '프로젝트 - 생성' }" class="ml-1">새 프로젝트</router-link>
      </span>
      <span>
        <v-icon icon="mdi-cog" color="secondary" size="sm" />
        <router-link :to="{ name: '프로젝트 목록' }" class="ml-1">관리</router-link>
      </span>
    </CCol>
  </CRow>

  <!--  <router-link :to="{ name: '(개요)', params: { projId: 'dongchun' } }">-->
  <!--    개별 프로젝트-->
  <!--  </router-link>-->
</template>
