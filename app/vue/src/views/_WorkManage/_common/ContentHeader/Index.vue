<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from '@/store'
import HeaderNav from '@/layouts/ContentHeader/components/HeaderNav.vue'

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
  <div class="mb-0 text-body" :class="backGround">
    <div class="mb-4 p-3 text-white">
      <v-icon icon="mdi mdi-text-box-check-outline" size="small" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </div>

    <div class="pl-5">
      <HeaderNav :menus="navMenu" :query="$route?.query" />
    </div>
  </div>
</template>
