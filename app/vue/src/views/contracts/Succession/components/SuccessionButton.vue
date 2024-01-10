<script lang="ts" setup>
import { AlertLight } from '@/utils/cssMixins'

defineProps({ isSuccession: { type: Boolean, default: false } })
const emit = defineEmits(['call-form'])

const callForm = () => emit('call-form')
</script>

<template>
  <CAlert :color="AlertLight" variant="solid" class="text-right">
    <CButton :color="isSuccession ? 'success' : 'primary'" @click="callForm">
      {{ isSuccession ? '수정하기' : '등록하기' }}
    </CButton>
  </CAlert>
</template>
