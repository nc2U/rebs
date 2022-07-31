<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { RouteLocationMatched } from 'vue-router'
import router from '@/router'

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
</script>

<template>
  <CBreadcrumb class="d-md-down-none me-auto mb-0">
    <!--    <TransitionGroup name="breadcrumb">-->
    <CBreadcrumbItem
      v-for="item in breadcrumbs"
      :key="item"
      :href="item.active ? '' : item.path"
      :active="item.active"
    >
      {{ item.name }}
    </CBreadcrumbItem>
    <!--    </TransitionGroup>-->
  </CBreadcrumb>
</template>
