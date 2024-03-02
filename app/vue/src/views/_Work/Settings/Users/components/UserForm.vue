<script lang="ts" setup="">
import { computed, inject, onBeforeMount } from 'vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import { useAccount } from '@/store/pinia/account'
import router from '@/router'

const superAuth = inject('superAuth', false)

const accStore = useAccount()
const user = computed(() => accStore.user)

onBeforeRouteUpdate(async to => {
  if (to.params.userId) await accStore.fetchUser(to.params.userId as string)
  else accStore.user = null
})
const route = useRoute()
onBeforeMount(() => {
  if (route.params.userId) accStore.fetchUser(route.params.userId)
  if (route.query.tab) router.replace({ name: '사용자 - 수정', params: { userId: user.value?.pk } })
})
</script>

<template>
  <CRow class="py-2">
    <CCol class="mb-2">
      <span class="h5 mr-2">
        <router-link :to="{ name: '사용자' }">사용자</router-link>
      </span>
      <span class="mr-2">»</span>
      <span class="h5">{{ user ? 'austin1' : '새 사용자' }}</span>
    </CCol>

    <CCol v-if="user && superAuth" class="text-right">
      <span class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '사용자 - 보기', params: { userId: user.pk } }" class="ml-1">
          사용자 정보
        </router-link>
      </span>
    </CCol>
  </CRow>

  <CRow v-if="user" class="mb-3">
    <CCol>
      <v-tabs density="compact">
        <v-tab
          :value="general"
          @click="
            $router.push({
              name: '사용자 - 수정',
              params: { userId: user.pk },
              query: { tab: 'general' },
            })
          "
        >
          일반
        </v-tab>
        <v-tab
          :value="project"
          @click="
            $router.push({
              name: '사용자 - 수정',
              params: { userId: user.pk },
              query: { tab: 'project' },
            })
          "
        >
          프로젝트
        </v-tab>
      </v-tabs>
    </CCol>
  </CRow>

  <CRow v-show="!$route?.query?.tab || $route.query?.tab === 'general'">
    <CCol>User Form</CCol>
  </CRow>

  <CRow v-show="$route?.query?.tab === 'project'">
    <CCol> 프로젝트 탭</CCol>
  </CRow>
</template>
