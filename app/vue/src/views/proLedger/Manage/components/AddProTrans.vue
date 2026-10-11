<script lang="ts" setup>
import { AlertLight } from '@/utils/cssMixins'

defineProps({ project: { type: Number, default: null } })

const emit = defineEmits<{
  (e: 'open-scraping'): void
}>()
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="d-flex justify-end ga-2">
    <v-btn
      color="indigo"
      variant="flat"
      :disabled="!project"
      prepend-icon="mdi-bank-transfer-in"
      @click="emit('open-scraping')"
    >
      은행 거래 AI 가져오기
    </v-btn>
    <v-btn
      color="primary"
      :disabled="!project"
      prepend-icon="mdi-plus"
      @click="$router.push({ name: '거래 내역 관리 - 생성' })"
    >
      새 거래 등록
    </v-btn>
  </CAlert>
</template>
