<script lang="ts" setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

defineProps({ contract: { type: Number, default: null } })

const [route, router] = [useRoute(), useRouter()]

const contractor = computed(() => route.query.contractor)

const isRegister = computed(() => route.name === '계약 등록 관리')
const isContorInfo = computed(() => route.name === '계약자 정보 변경')
const isSuccession = computed(() => route.name === '권리 의무 승계')
const isRelease = computed(() => route.name === '계약 해지 관리')
</script>

<template>
  <CButtonGroup role="group" aria-label="Basic example" class="mb-3">
    <CButton
      :color="isRegister ? 'primary' : 'light'"
      :disabled="!contract || !contractor"
      @click="
        router.push({
          name: '계약 등록 관리',
          query: { contractor },
        })
      "
    >
      계약 등록 관리
    </CButton>
    <CButton :color="isContorInfo ? 'info' : 'light'" disabled>
      계약자 정보 변경
    </CButton>
    <CButton
      :color="isSuccession ? 'success' : 'light'"
      :disabled="!contract || !contractor"
      @click="
        router.push({
          name: '권리 의무 승계',
          query: { contractor },
        })
      "
    >
      권리 의무 승계
    </CButton>
    <CButton
      :color="isRelease ? 'danger' : 'light'"
      :disabled="!contractor"
      @click="
        router.push({
          name: '계약 해지 관리',
          query: { contractor },
        })
      "
    >
      계약 해지 관리
    </CButton>
  </CButtonGroup>
</template>
