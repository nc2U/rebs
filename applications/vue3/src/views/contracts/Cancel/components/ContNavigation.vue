<template>
  <CButtonGroup role="group" aria-label="Basic example" class="mb-3">
    <CButton
      color="light"
      @click="
        $router.push({
          name: '계약등록 관리',
          query: { contract: contractor.contract },
        })
      "
      :disabled="!contractor || contractor.status > '2'"
    >
      등록 계약 변경
    </CButton>
    <CButton color="light" disabled>권리 의무 승계</CButton>
    <CButton color="light" disabled>주소(연락처) 변경</CButton>
    <CButton color="primary">계약 해지 관리</CButton>
  </CButtonGroup>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContNavigation',
  props: { contractor: Object },
})
</script>
