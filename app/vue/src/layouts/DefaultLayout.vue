<script lang="ts" setup>
import { CContainer } from '@coreui/vue'
import AppSidebar from '@/layouts/containers/AppSidebar.vue'
import AppHeader from '@/layouts/containers/AppHeader.vue'
import AppFooter from '@/layouts/containers/AppFooter.vue'
import AppAside from '@/layouts/containers/AppAside.vue'
import BackToTop from '@/components/BackToTop/index.vue'
</script>

<template>
  <AppSidebar />
  <div class="wrapper d-flex flex-column min-vh-100 bg-light dark:bg-body">
    <AppHeader />
    <!--    <div class="body flex-grow-1 px-md-3 px-xl-5">-->
    <div class="body flex-grow-1" style="display: flex; align-items: stretch">
      <CContainer fluid class="p-0" style="flex: 1">
        <router-view />
      </CContainer>
    </div>
    <AppFooter />
  </div>
  <AppAside />
  <BackToTop />
</template>
