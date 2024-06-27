<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/_Work/_menu/headermixin3'
import { useAccount } from '@/store/pinia/account'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import UserList from '@/views/_Work/Settings/Users/components/UserList.vue'
import UserView from '@/views/_Work/Settings/Users/components/UserView.vue'
import UserForm from '@/views/_Work/Settings/Users/components/UserForm.vue'

const cBody = ref()
const aside = ref(true)

const asideVisible = (visible: boolean) => (aside.value = visible)

const sideNavCAll = () => cBody.value.toggle()

const accStore = useAccount()
const usersList = computed(() => accStore.usersList)
onBeforeMount(() => accStore.fetchUsersList())
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query" :aside="aside">
    <template v-slot:default>
      {{ aside }}
      <UserList
        v-if="$route.name === '사용자'"
        :user-list="usersList"
        @aside-visible="asideVisible"
      />

      <UserView v-else-if="$route.name === '사용자 - 보기'" @aside-visible="asideVisible" />

      <UserForm v-else-if="$route.name === '사용자 - 생성'" @aside-visible="asideVisible" />

      <UserForm v-else-if="$route.name === '사용자 - 수정'" @aside-visible="asideVisible" />
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
