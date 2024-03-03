<script lang="ts" setup>
import { useAccount } from '@/store/pinia/account'
import { computed, inject, onBeforeMount } from 'vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'

const superAuth = inject('superAuth', false)

const accStore = useAccount()
const user = computed(() => accStore.user)

onBeforeRouteUpdate(async to => {
  if (to.params.userId) await accStore.fetchUser(Number(to.params.userId))
  else accStore.user = null
})
const route = useRoute()
onBeforeMount(() => {
  if (route.params.userId) accStore.fetchUser(Number(route.params.userId))
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="h5 mr-2">
        {{ user?.username }}
      </span>
    </CCol>

    <CCol v-if="user && superAuth" class="text-right">
      <span class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '사용자 - 수정', params: { userId: user.pk } }" class="ml-1">
          편집
        </router-link>
      </span>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <ul>
        <li>로그인 :</li>
        <li>등록시각 :</li>
        <li>마지막 로그인 :</li>
      </ul>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <h6>업무</h6>
    </CCol>
  </CRow>
</template>
