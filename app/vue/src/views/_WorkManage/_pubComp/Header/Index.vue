<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from '@/store'
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
  <CRow class="mb-0 text-body" :class="backGround">
    <CCol>
      <CRow>
        <CCol class="mb-2 p-4 text-white">
          <strong class="title pl-1"> {{ pageTitle }}</strong>
        </CCol>
        <CCol class="text-right p-3 pr-4">
          <v-icon icon="mdi-text" size="x-large" class="d-md-none pointer" @click="sideNavCall" />
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
}
</style>
