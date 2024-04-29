<script lang="ts" setup>
import { inject } from 'vue'

const isDark = inject('isDark')
</script>

<template>
  <CCard :color="isDark ? '' : 'light'">
    <CCardBody>
      <h6>
        <v-icon icon="mdi-clock-outline" size="small" />
        시간추적
      </h6>
      <ul class="pl-4 mb-0">
        <li>추정시간 : 48:00 시간</li>
        <li>소요시간 : 0:00 시간</li>
      </ul>
    </CCardBody>

    <CCardText class="mx-3 mb-2 form-text">
      <router-link :to="{ name: '(소요시간) - 추가' }">작업시간 기록</router-link>

      <span class="px-2">|</span>
      <router-link :to="{ name: '(소요시간)' }">자세히</router-link>
      <span class="px-2">|</span>
      <router-link :to="{ name: '(소요시간) - 보고서' }">보고서</router-link>
    </CCardText>
  </CCard>
</template>
