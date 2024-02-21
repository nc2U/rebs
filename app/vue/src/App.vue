<script lang="ts" setup>
import { computed, provide, watch, onMounted } from 'vue'
import { useStore } from '@/store'
import { useAccount } from '@/store/pinia/account'
import { useCompany } from '@/store/pinia/company'

const accStore = useAccount()
const userInfo = computed(() => accStore.userInfo)
const superAuth = computed(() => accStore.superAuth)
provide('userInfo', userInfo)
provide('superAuth', superAuth)

const comStore = useCompany()
const company = computed(() => comStore.company?.pk)
provide('comStore', comStore)

const store = useStore()
watch(store, () => {
  store.theme === 'dark'
    ? document.body.classList.add('dark-theme')
    : document.body.classList.remove('dark-theme')
})

onMounted(() => {
  store.theme === 'dark'
    ? document.body.classList.add('dark-theme')
    : document.body.classList.remove('dark-theme')
  if (accStore.isAuthorized) comStore.fetchCompany(company.value || comStore.initComId)
})
</script>

<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
