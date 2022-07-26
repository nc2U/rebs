<script lang="ts" setup>
import { CContainer } from '@coreui/vue-pro'
import AppAside from '@/layouts/containers/AppAside.vue'
import AppFooter from '@/layouts/containers/AppFooter.vue'
import AppHeader from '@/layouts/containers/AppHeader.vue'
import AppSidebar from '@/layouts/containers/AppSidebar.vue'
import BackToTop from '@/components/BackToTop/index.vue'
</script>

<template>
  <AppSidebar />
  <div
    class="wrapper d-flex flex-column min-vh-100 bg-light dark:bg-transparent"
  >
    <AppHeader />
    <div class="body flex-grow-1 px-3">
      <CContainer fluid>
        <router-view />
      </CContainer>
    </div>
    <AppFooter />
    <BackToTop />
  </div>
  <AppAside />
</template>
