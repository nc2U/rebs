<script lang="ts" setup>
import type { RouteRecordName } from 'vue-router'

defineProps({
  menus: { type: Array, required: true },
  query: { type: Object, default: null },
})
</script>

<template>
  <CNav variant="tabs" class="mb-0 pl-4">
    <CDropdown color="secondary" class="m-0">
      <CDropdownToggle component="button" color=""></CDropdownToggle>
      <CDropdownMenu>
        <CDropdownItem>새 업무 만들기</CDropdownItem>
        <CDropdownItem>새 업무 카테고리</CDropdownItem>
        <CDropdownItem>새 버전</CDropdownItem>
        <CDropdownItem>작업시간 기록</CDropdownItem>
        <CDropdownItem>새 뉴스</CDropdownItem>
        <CDropdownItem>새 문서</CDropdownItem>
        <CDropdownItem>새 위키</CDropdownItem>
        <CDropdownItem>파일추가</CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
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
