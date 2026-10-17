<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Building from './Building.vue'
import type { SimpleUnit } from './ContractBoard.vue'

defineProps<{
  bldg: number
  maxFloor: number
  units: SimpleUnit[]
}>()

const hasBeenVisible = ref(false) // 한 번 로드되면 유지
const container = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | null = null

onMounted(() => {
  if (typeof window !== 'undefined' && 'IntersectionObserver' in window) {
    observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            hasBeenVisible.value = true
            if (observer && container.value) {
              observer.unobserve(container.value)
            }
          }
        })
      },
      {
        rootMargin: '300px', // 뷰포트 300px 전에 미리 로드
        threshold: 0.01,
      },
    )

    if (container.value) {
      observer.observe(container.value)
    }
  } else {
    // IntersectionObserver 미지원 환경 fallback
    hasBeenVisible.value = true
  }
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
    observer = null
  }
})
</script>

<template>
  <div ref="container" class="lazy-building-wrapper">
    <Building v-if="hasBeenVisible" :bldg="bldg" :max-floor="maxFloor" :units="units" />
    <div v-else class="loading-placeholder">
      <CSpinner size="sm" color="primary" />
      <span class="ms-2 text-muted">로딩 중...</span>
    </div>
  </div>
</template>

<style scoped>
.lazy-building-wrapper {
  display: inline-block;
  min-height: 100px;
  min-width: 100px;
}

.loading-placeholder {
  min-height: 100px;
  min-width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  opacity: 0.6;
}
</style>
