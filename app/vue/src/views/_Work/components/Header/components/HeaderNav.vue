<script lang="ts" setup>
import { computed, inject } from 'vue'
import { useStore } from '@/store'
import { type RouteRecordName } from 'vue-router'

defineProps({
  menus: { type: Array, required: true },
  query: { type: Object, default: null },
})

const superAuth = inject('superAuth')

const store = useStore()
const isDark = computed(() => store.theme === 'dark')

const getTitle = (title: string) => title.replace(/[() ]/gim, '')
</script>

<template>
  <CNav variant="tabs" class="mb-0 pl-4">
    <CDropdown v-if="$route.params['projId']">
      <CDropdownToggle :color="isDark ? 'dark' : 'light'" />
      <CDropdownMenu>
        <CDropdownItem @click="$router.push({ name: '(업무) - 추가' })">
          새 업무 만들기
        </CDropdownItem>
        <CDropdownItem v-if="superAuth" disabled>새 업무 카테고리</CDropdownItem>
        <CDropdownItem v-if="superAuth" disabled>새 버전</CDropdownItem>
        <CDropdownItem v-if="superAuth" @click="$router.push({ name: '(소요시간) - 추가' })">
          작업시간 기록
        </CDropdownItem>
        <CDropdownItem v-if="superAuth" disabled>새 뉴스</CDropdownItem>
        <CDropdownItem v-if="superAuth" disabled>새 문서</CDropdownItem>
        <CDropdownItem v-if="superAuth" disabled>새 위키</CDropdownItem>
        <CDropdownItem v-if="superAuth" disabled>파일추가</CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
    <CNavItem v-for="(menu, i) in menus" :key="i">
      <CNavLink
        :active="
          ($route.name as string).includes(menu as string) ||
          ($route.meta.title as string).includes(menu as string)
        "
        @click="$router.push({ name: menu as RouteRecordName, query })"
      >
        {{ getTitle(menu as string) }}
      </CNavLink>
    </CNavItem>
  </CNav>
</template>
