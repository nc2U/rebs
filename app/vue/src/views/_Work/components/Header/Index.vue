<script lang="ts" setup>
import { ref, computed, type PropType } from 'vue'
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
  parents: {
    type: Array as PropType<{ pk: number; name: string; slug: string }[]>,
    default: () => [],
  },
})

const visible = ref(false)

const isDark = computed(() => useStore().theme === 'dark')
const backGround = computed(() => (isDark.value ? 'bg-blue-grey-darken-5' : 'bg-indigo-lighten-5'))

const emit = defineEmits(['side-nav-call'])
const sideNavCall = () => emit('side-nav-call')
</script>

<template>
  <CRow class="mb-0" :class="backGround">
    <CCol>
      <CRow class="px-3">
        <CCol class="mb-2 p-4 col-9 col-md-6 col-lg-7 col-xl-9">
          <CRow v-if="!!parents.length" class="d-none d-md-block">
            <CCol>
              <span v-for="p in parents" :key="p.pk" class="mr-1 text-blue-grey">
                <router-link :to="{ name: '(개요)', params: { projId: p.slug } }">
                  {{ p.name }}
                </router-link>
                »
              </span>
            </CCol>
          </CRow>
          <CRow>
            <CCol class="text-body d-none d-md-block">
              <strong class="title pl-1"> {{ pageTitle }}</strong>
            </CCol>

            <CCol
              class="text-body d-md-none"
              :class="{ pointer: !!parents.length }"
              @click="visible = !visible"
            >
              <v-icon
                v-if="!!parents.length"
                :icon="visible ? 'mdi-chevron-up' : 'mdi-chevron-down'"
                color=""
              />
              <strong class="title pl-1"> {{ pageTitle }}</strong>
              <CCollapse v-if="!!parents.length" :visible="visible">
                <CCard class="mt-3">
                  <CCardBody>
                    <span v-for="p in parents" :key="p.pk" class="mr-1 text-blue-grey">
                      <router-link :to="{ name: '(개요)', params: { projId: p.slug } }">
                        {{ p.name }}
                      </router-link>
                      »
                    </span>
                  </CCardBody>
                </CCard>
              </CCollapse>
            </CCol>
          </CRow>
        </CCol>

        <CCol class="text-body d-md-none text-right p-3">
          <v-icon icon="mdi-view-headline" size="x-large" class="pointer" @click="sideNavCall" />
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
  color: #5e636a;
}

.dark-theme .title {
  color: #ddd;
}
</style>
