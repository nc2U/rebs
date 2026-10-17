<script lang="ts" setup>
import { AlertLight } from '@/utils/cssMixins'

defineProps<{
  company?: number | null
}>()

const emit = defineEmits<{
  (e: 'open-scraping'): void
  (e: 'open-register'): void
}>()
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="d-flex justify-end ga-2">
    <v-btn
      color="indigo-darken-2"
      variant="tonal"
      :disabled="!company"
      prepend-icon="mdi-shield-key-outline"
      @click="emit('open-register')"
    >
      공동인증서/계좌 연동
    </v-btn>
    <v-btn
      color="indigo"
      variant="flat"
      :disabled="!company"
      prepend-icon="mdi-bank-transfer-in"
      @click="emit('open-scraping')"
    >
      은행 거래 AI 가져오기
    </v-btn>
    <v-btn
      color="primary"
      :disabled="!company"
      prepend-icon="mdi-plus"
      @click="$router.push({ name: '본사 거래 내역 - 생성' })"
    >
      새 거래 등록
    </v-btn>
  </CAlert>
</template>
