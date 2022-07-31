<script lang="ts" setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import AppBreadcrumb from './AppBreadcrumb.vue'
import AppHeaderDropdownAccnt from './AppHeaderDropdownAccnt.vue'
import { directive as vFullscreen } from 'vue-fullscreen'
import { logo } from '@/assets/brand/current-logo'
import TagsView from '@/layouts/containers/TagsView/index.vue'

const store = useStore()
const screenIcon = ref('mdi-fullscreen')
const screenGuide = ref('전체화면')
const options = ref({
  target: '.fullscreen-wrapper',
  callback(isFullscreen: boolean) {
    screenIcon.value = !isFullscreen ? 'mdi-fullscreen' : 'mdi-fullscreen-exit'
    screenGuide.value = !isFullscreen ? '전체화면' : '전체화면 종료'
  },
})
const userInfo = store.state.accounts.userInfo
const isAuthorized = store.getters['accounts/isAuthorized']
</script>

<template>
  <CHeader position="sticky" class="mb-4 pb-0">
    <CContainer fluid>
      <CHeaderToggler class="ps-1" @click="$store.commit('toggleSidebar')">
        <CIcon icon="cil-menu" size="lg" />
      </CHeaderToggler>
      <CHeaderBrand class="mx-auto d-lg-none" to="/">
        <CIcon :icon="logo" height="48" alt="Logo" />
      </CHeaderBrand>
      <CHeaderNav class="d-none d-lg-flex me-auto">
        <AppBreadcrumb />
      </CHeaderNav>
      <CHeaderNav class="ms-auto me-4">
        <CHeaderToggler v-fullscreen.teleport="options">
          <v-icon large :icon="screenIcon" />
          <v-tooltip activator="parent" location="bottom">
            {{ screenGuide }}
          </v-tooltip>
        </CHeaderToggler>
        <CButtonGroup aria-label="Theme switch">
          <CFormCheck
            id="btn-light-theme"
            type="radio"
            :button="{ color: 'primary' }"
            name="theme-switch"
            auto-complete="off"
            :checked="$store.state.theme === 'default'"
            @change="
              event =>
                $store.commit({
                  type: 'toggleTheme',
                  value: 'default',
                })
            "
          >
            <template #label>
              <CIcon icon="cil-sun" />
            </template>
          </CFormCheck>
          <CFormCheck
            id="btn-dark-theme"
            type="radio"
            :button="{ color: 'primary' }"
            name="theme-switch"
            auto-complete="off"
            :checked="$store.state.theme === 'dark'"
            @change="
              event =>
                $store.commit({
                  type: 'toggleTheme',
                  value: 'dark',
                })
            "
          >
            <template #label>
              <CIcon icon="cil-moon" />
            </template>
          </CFormCheck>
        </CButtonGroup>
      </CHeaderNav>
      <CHeaderNav class="ms-3 me-4">
        <AppHeaderDropdownAccnt
          v-if="isAuthorized && userInfo"
          :user-info="userInfo"
        />
        <router-link
          v-else
          :to="{ name: 'Login' }"
          class="btn btn-outline-primary"
        >
          로그인
        </router-link>
      </CHeaderNav>
      <CHeaderToggler class="px-md-0 me-md-3">
        <CIcon
          icon="cil-applications-settings"
          size="lg"
          @click="$store.commit('toggleAside')"
        />
      </CHeaderToggler>
    </CContainer>
    <CHeaderDivider class="mb-0" />
    <CContainer fluid class="px-3">
      <TagsView />
    </CContainer>
  </CHeader>
</template>
