<script lang="ts" setup>
import { onMounted, provide, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { useStore } from '@/store'

const accStore = useAccount()
provide('userInfo', accStore.userInfo)

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
