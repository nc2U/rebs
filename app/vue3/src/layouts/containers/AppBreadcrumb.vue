<template>
  <CBreadcrumb class="d-md-down-none me-auto mb-0">
    <CBreadcrumbItem
      v-for="item in breadcrumbs"
      :href="item.active ? '' : item.path"
      :active="item.active"
      :key="item"
    >
      {{ item.name }}
    </CBreadcrumbItem>
  </CBreadcrumb>
</template>

<script lang="ts">
import { onMounted, ref } from 'vue'
import { RouteLocationMatched } from 'vue-router'
import router from '@/router'

export default {
  name: 'AppBreadcrumb',
  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  setup() {
    const breadcrumbs = ref()

    const getBreadcrumbs = () => {
      return router.currentRoute.value.matched.map(
        (route: RouteLocationMatched) => {
          return {
            active: route.path === router.currentRoute.value.fullPath,
            name: route.name,
            path: `${router.options.history.base}${route.path}`,
          }
        },
      )
    }

    router.afterEach(() => {
      breadcrumbs.value = getBreadcrumbs()
    })

    onMounted(() => {
      breadcrumbs.value = getBreadcrumbs()
    })

    return {
      breadcrumbs,
    }
  },
}
</script>
