<script lang="ts" setup>
import { type RouteRecordName, useRoute, useRouter } from 'vue-router'

defineProps({
  menus: { type: Array, required: true },
  query: { type: Object, default: null },
})

const [route, router] = [useRoute(), useRouter()]
</script>

<template>
  <CNav variant="tabs" class="mb-5">
    <CNavItem v-for="(menu, i) in menus" :key="i">
      <CNavLink
        :active="route.name === menu || route.meta.title === menu"
        @click="router.push({ name: menu as RouteRecordName, query })"
      >
        {{ menu }}
      </CNavLink>
    </CNavItem>
  </CNav>
</template>
