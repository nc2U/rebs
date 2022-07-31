<template>
  <CNav variant="tabs" class="mb-5">
    <CNavItem v-for="(menu, i) in menus" :key="i">
      <CNavLink
        @click="$router.push({ name: menu })"
        :active="$route.name == menu"
      >
        {{ menu }}
      </CNavLink>
    </CNavItem>
  </CNav>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'HeadNav',
  props: {
    menus: {
      type: Array,
      required: true,
    },
  },
})
</script>
