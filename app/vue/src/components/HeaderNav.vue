<script lang="ts" setup>
defineProps({ menus: { type: Array, required: true } })
</script>

<template>
  <CNav variant="tabs" class="mb-5">
    <CNavItem v-for="(menu, i) in menus" :key="i">
      <CNavLink
        :active="$route.name === menu || $route.meta.title === menu"
        @click="$router.push({ name: menu })"
      >
        {{ menu }}
      </CNavLink>
    </CNavItem>
  </CNav>
</template>
