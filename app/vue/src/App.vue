<script lang="ts" setup>
import { watch } from 'vue'
import { useStore } from 'vuex'
import Spinner from '@/components/Spinner/index.vue'

const store = useStore()

watch(store.state, () => {
  store.state.theme === 'dark'
    ? document.body.classList.add('dark-theme')
    : document.body.classList.remove('dark-theme')
})

store.state.theme === 'dark'
  ? document.body.classList.add('dark-theme')
  : document.body.classList.remove('dark-theme')
</script>

<template>
  <v-app>
    <v-main>
      <router-view />
      <Spinner :loading="$store.state.LoadingStatus" />
    </v-main>
  </v-app>
</template>
