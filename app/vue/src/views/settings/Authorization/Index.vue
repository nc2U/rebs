<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { useAccount } from '@/store/pinia/account'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UserSelect from './components/UserSelect.vue'
import ProjectManageAuth from './components/ProjectManageAuth.vue'
import SideBarManageAuth from './components/SideBarManageAuth.vue'

const accountStore = useAccount()
const user = computed(() => accountStore.user)
const userInfo = computed(() => accountStore.userInfo)

const selectUser = (pk: number | null) => {
  if (pk === null) accountStore.user = null
  else accountStore.fetchUser(pk)
}
const getAllowed = (payload: any) => console.log(payload)
const getAssigned = (payload: any) => console.log(payload)
const selectAuth = (payload: any) => console.log(payload)

onBeforeMount(() => {
  accountStore.fetchUsersList()
  if (userInfo.value) selectUser(userInfo.value.pk as number)
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody>
    <CCardBody>
      <UserSelect @select-user="selectUser" />
      <ProjectManageAuth :user="user" @get-allowed="getAllowed" />
      <SideBarManageAuth
        :user="user"
        @get-assigned="getAssigned"
        @select-auth="selectAuth"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
