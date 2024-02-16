<script lang="ts" setup>
import type { RouteRecordName } from 'vue-router'

defineProps({
  menus: { type: Array, required: true },
  query: { type: Object, default: null },
})
</script>

<template>
  <CNav variant="tabs">
    <CNavItem v-for="(menu, i) in menus" :key="i">
      <CNavLink
        :active="$route.name === menu || $route.meta.title === menu"
        @click="$router.push({ name: menu as RouteRecordName, query })"
      >
        {{ menu }}
      </CNavLink>
    </CNavItem>
  </CNav>
</template>
