<script lang="ts" setup>
import { ref } from 'vue'
import { type RouteRecordName, useRouter } from 'vue-router'

const props = defineProps({
  navMenu: {
    type: Array,
    default: () => [],
  },
  query: { type: Object, default: null },
})
const visible = ref(false)

const router = useRouter()

const goToMenu = (menu: string) => {
  router.push({ name: menu as RouteRecordName, query: props.query })
  visible.value = false
}
const toggle = () => (visible.value = !visible.value)
defineExpose({ toggle })
</script>

<template>
  <CRow class="flex-grow-1">
    <CCol md="9" class="text-body pl-5 p-3 main">
      <slot></slot>
    </CCol>

    <CCol class="text-body p-3 d-none d-md-block">
      <slot name="aside"></slot>
    </CCol>

    <COffcanvas
      placement="end"
      class="p-2"
      :visible="visible"
      @hide="
        () => {
          visible = !visible
        }
      "
    >
      <COffcanvasHeader>
        <COffcanvasTitle>
          <CFormInput placeholder="검색" />
        </COffcanvasTitle>
        <CCloseButton
          class="text-reset"
          @click="
            () => {
              visible = false
            }
          "
        />
      </COffcanvasHeader>

      <v-divider />

      <COffcanvasBody class="p-0">
        <CRow class="mb-3">
          <CCol class="d-grid gap-2">
            <CNavbarNav vertical role="group" aria-label="Vertical button group" class="m-0">
              <CNavItem v-for="(menu, i) in navMenu" :key="i">
                <CNavLink
                  @click="goToMenu(menu as string)"
                  :active="$route.name === menu || $route.meta.title === menu"
                  class="pl-3"
                >
                  {{ menu }}
                </CNavLink>
              </CNavItem>
            </CNavbarNav>
          </CCol>
        </CRow>

        <v-divider />

        <slot name="aside">
          Content for the offcanvas goes here. You can place just about any Bootstrap component or
          custom elements here.
        </slot>
      </COffcanvasBody>
    </COffcanvas>
  </CRow>
</template>

<style lang="scss" scoped>
.main {
  background: #ffffff;
  border-right: 1px solid #ddd !important;
}

.dark-theme .main {
  background: #151620;
  border-right: 1px solid #333 !important;
}

.active {
  font-weight: bold;
  background: #e5e7eb;
}

.dark-theme .active {
  background: #32333d;
}
</style>