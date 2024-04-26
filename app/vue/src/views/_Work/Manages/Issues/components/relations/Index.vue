<script lang="ts" setup>
import { ref } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const msg = ref('Hello world')
</script>

<template>
  <div>{{ msg }}</div>

  <ConfirmModal ref="delRelRef">
    <template #header>관계 지우기 확인</template>
    <template #default> 계속 진행하시겠습니까?</template>
    <template #footer>
      <CButton color="warning" @click="unLinkRelConfirm">확인</CButton>
    </template>
  </ConfirmModal>
</template>
