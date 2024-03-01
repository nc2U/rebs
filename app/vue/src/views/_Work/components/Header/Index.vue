<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from '@/store'
import HeaderSearch from './components/Search.vue'
import HeaderNav from './components/HeaderNav.vue'

defineProps({
  pageTitle: {
    type: String,
    default: 'Page Title',
  },
  navMenu: {
    type: Array,
    default: () => ['Base Menu'],
  },
})

const isDark = computed(() => useStore().theme === 'dark')
const backGround = computed(() =>
  isDark.value ? 'bg-blue-grey-darken-5' : 'bg-blue-grey-lighten-4',
)

const emit = defineEmits(['side-nav-call'])
const sideNavCall = () => emit('side-nav-call')
</script>

<template>
  <CRow class="mb-0" :class="backGround">
    <CCol>
      <CRow class="px-3">
        <CCol class="mb-2 p-4">
          <strong class="title pl-1"> {{ pageTitle }}</strong>
        </CCol>
        <CCol class="text-right p-3 pr-5">
          <v-icon
            icon="mdi-view-headline"
            size="x-large"
            class="d-md-none pointer"
            @click="sideNavCall"
          />
        </CCol>
        <CCol class="d-none d-md-block text-right">
          <HeaderSearch />
        </CCol>
      </CRow>
      <CRow class="d-none d-md-block">
        <CCol>
          <HeaderNav :menus="navMenu" :query="$route?.query" />
        </CCol>
      </CRow>
    </CCol>
  </CRow>
</template>

<style lang="scss" scoped>
strong.title {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 20px;
  color: #456;
}

.dark-theme .title {
  color: #ddd;
}
</style>
