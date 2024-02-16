<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from '@/store'

const isDark = computed(() => useStore().theme === 'dark')
const backGround = computed(() => (isDark.value ? '' : 'bg-white'))
</script>

<template>
  <div class="mt-0 mb-4 text-body" :class="backGround">a</div>
</template>
