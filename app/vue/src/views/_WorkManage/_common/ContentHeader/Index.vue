<script lang="ts" setup>
import HeaderNav from '@/layouts/ContentHeader/components/HeaderNav.vue'
import { computed } from 'vue'
import { useStore } from '@/store'

defineProps({
  pageTitle: {
    type: String,
    default: 'Page Title',
  },
  navMenu: {
    type: Array,
    default: () => ['Base Menu'],
  },
})

const isDark = computed(() => useStore().theme === 'dark')
const backGround = computed(() =>
  isDark.value ? 'bg-blue-grey-darken-3' : 'bg-blue-grey-lighten-3',
)
</script>

<template>
  <div class="mb-4 text-body" :class="backGround">
    <div class="mb-4 p-3 text-white">
      <v-icon icon="mdi mdi-text-box-check-outline" size="small" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </div>

    <div class="pl-5">
      <HeaderNav :menus="navMenu" :query="$route?.query" />

      <slot />
    </div>
  </div>
</template>
