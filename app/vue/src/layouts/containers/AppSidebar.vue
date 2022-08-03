<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { AppSidebarNav } from './AppSidebarNav'
import { logoNegative, sygnet } from '@/assets/brand/current-logo'

const store = useStore()

const sidebarUnfoldable = computed(() => store.state.sidebarUnfoldable)
const sidebarVisible = computed(() => store.state.sidebarVisible)
</script>

<template>
  <CSidebar
    position="fixed"
    self-hiding="md"
    :unfoldable="sidebarUnfoldable"
    :visible="sidebarVisible"
    @visible-change="
      event =>
        store.commit({
          type: 'updateSidebarVisible',
          value: event,
        })
    "
  >
    <CSidebarBrand>
      <CIcon
        custom-class-name="sidebar-brand-full"
        :icon="logoNegative"
        :height="35"
      />
      <CIcon
        custom-class-name="sidebar-brand-narrow"
        :icon="sygnet"
        :height="35"
      />
    </CSidebarBrand>
    <AppSidebarNav />
    <CSidebarToggler
      class="d-none d-lg-flex"
      @click="store.commit('toggleUnfoldable')"
    />
  </CSidebar>
</template>
