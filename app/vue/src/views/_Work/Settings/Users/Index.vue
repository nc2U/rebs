<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/_Work/_menu/headermixin3'
import { useAccount } from '@/store/pinia/account'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import UserList from '@/views/_Work/Settings/Users/components/UserList.vue'

const cBody = ref()
const sideNavCAll = () => cBody.value.toggle()

const accStore = useAccount()
const usersList = computed(() => accStore.usersList)
onBeforeMount(() => accStore.fetchUsersList())
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <UserList :user-list="usersList" />
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
