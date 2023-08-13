<script lang="ts" setup>
import { onMounted, watch } from 'vue'
import { useStore } from '@/store'

const store = useStore()

watch(store, () => {
  store.theme === 'dark'
    ? document.body.classList.add('dark-theme')
    : document.body.classList.remove('dark-theme')
})

onMounted(() =>
  store.theme === 'dark'
    ? document.body.classList.add('dark-theme')
    : document.body.classList.remove('dark-theme'),
)
</script>

<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
