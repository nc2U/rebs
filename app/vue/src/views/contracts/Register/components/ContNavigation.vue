<script lang="ts" setup>
defineProps({ contractor: { type: Number, default: null } })
</script>

<template>
  <CButtonGroup role="group" aria-label="Basic example" class="mb-3">
    <CButton color="primary"> 등록 계약 변경</CButton>
    <CButton color="light" disabled>권리 의무 승계</CButton>
    <CButton color="light" disabled>주소(연락처) 변경</CButton>
    <CButton
      color="light"
      @click="
        $router.push({
          name: '계약 해지 관리',
          query: { contractor },
        })
      "
    >
      계약 해지 관리
    </CButton>
  </CButtonGroup>
</template>
