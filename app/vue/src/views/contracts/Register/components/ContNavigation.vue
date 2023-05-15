<script lang="ts" setup>
import { useRoute, useRouter } from 'vue-router'

const [route, router] = [useRoute(), useRouter()]
</script>

<template>
  <CButtonGroup role="group" aria-label="Basic example" class="mb-3">
    <CButton color="primary"> 등록 계약 변경</CButton>
    <CButton color="light" disabled>주소(연락처) 변경</CButton>
    <CButton
      color="light"
      :disabled="!route.query.contract"
      @click="
        router.push({
          name: '권리 의무 승계',
          query: { contract: route.query.contract },
        })
      "
    >
      권리 의무 승계
    </CButton>
    <CButton
      color="light"
      :disabled="!route.query.contract"
      @click="
        router.push({
          name: '계약 해지 관리',
          query: { contract: route.query.contract },
        })
      "
    >
      계약 해지 관리
    </CButton>
  </CButtonGroup>
</template>
