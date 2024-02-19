<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from '@/store'
import HeaderNav from './components/HeaderNav.vue'

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
  isDark.value ? 'bg-blue-grey-darken-5' : 'bg-blue-grey-lighten-4',
)
</script>

<template>
  <div class="mb-0 text-body" :class="backGround">
    <div class="mb-2 p-4 text-white">
      <strong class="title pl-1"> {{ pageTitle }}</strong>
    </div>

    <div class="pl-5">
      <HeaderNav :menus="navMenu" :query="$route?.query" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
strong.title {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 20px;
}
</style>
