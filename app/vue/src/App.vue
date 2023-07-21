<script lang="ts" setup>
import { onMounted, watch } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

watch(store.state, () => {
  store.state.theme === 'dark'
    ? document.body.classList.add('dark-theme')
    : document.body.classList.remove('dark-theme')
})

onMounted(() =>
  store.state.theme === 'dark'
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
