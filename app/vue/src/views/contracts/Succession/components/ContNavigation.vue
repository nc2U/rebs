<script lang="ts" setup>
defineProps({ contractor: { type: Object, default: null } })
</script>

<template>
  <CButtonGroup role="group" aria-label="Basic example" class="mb-3">
    <CButton
      color="light"
      :disabled="!contractor || contractor.status > '2'"
      @click="
        $router.push({
          name: '계약 등록 관리',
          query: { contract: contractor.contract },
        })
      "
    >
      등록 계약 변경
    </CButton>
    <CButton color="light" disabled>주소(연락처) 변경</CButton>
    <CButton color="success">권리 의무 승계</CButton>
    <CButton
      color="light"
      @click="
        $router.push({
          name: '계약 해지 관리',
          query: { contract: contractor.contract },
        })
      "
      >계약 해지 관리
    </CButton>
  </CButtonGroup>
</template>
