<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { useAccount } from '@/store/pinia/account'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UserSelect from './components/UserSelect.vue'
import ProjectManageAuth from './components/ProjectManageAuth.vue'
import SideBarManageAuth from './components/SideBarManageAuth.vue'

const projectAuth = ref({
  is_staff: true,
  assigned_project: null as number | null,
  allowed_projects: [] as number[],
})

type Auth = '0' | '1' | '2'
export type MenuType = {
  contract: Auth
  payment: Auth
  notice: Auth
  project: Auth
  project_cash: Auth
  project_docs: Auth
  human_resource: Auth
  company_settings: Auth
  company_cash: Auth
  company_docs: Auth
  auth_manage: Auth
}
const menuAuth = ref<MenuType>({
  contract: '0',
  payment: '0',
  notice: '0',
  project: '0',
  project_cash: '0',
  project_docs: '0',
  human_resource: '0',
  company_settings: '0',
  company_cash: '0',
  company_docs: '0',
  auth_manage: '0',
})

const accountStore = useAccount()
const user = computed(() => accountStore.user)
const userInfo = computed(() => accountStore.userInfo)

const selectUser = (pk: number | null) => {
  if (pk === null) accountStore.user = null
  else accountStore.fetchUser(pk)
}
const getAllowed = (payload: number[]) =>
  (projectAuth.value.allowed_projects = payload)
const getAssigned = (payload: number | null) =>
  (projectAuth.value.assigned_project = payload)
const selectAuth = (payload: MenuType) => (menuAuth.value = payload)

onBeforeMount(() => {
  accountStore.fetchUsersList()
  if (userInfo.value) selectUser(userInfo.value.pk as number)
})

watch(
  () => user.value,
  nv => {
    const au = nv?.staffauth
    if (nv && au) {
      projectAuth.value.assigned_project = au.assigned_project
      projectAuth.value.allowed_projects = au.allowed_projects
      menuAuth.value.contract = au.contract
      menuAuth.value.payment = au.payment
      menuAuth.value.notice = au.notice
      menuAuth.value.project_cash = au.project_cash
      menuAuth.value.project_docs = au.project_docs
      menuAuth.value.project = au.project
      menuAuth.value.company_cash = au.company_cash
      menuAuth.value.company_docs = au.company_docs
      menuAuth.value.human_resource = au.human_resource
      menuAuth.value.company_settings = au.company_settings
      menuAuth.value.auth_manage = au.auth_manage
    }
  },
)
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
      <ProjectManageAuth
        :user="user"
        @get-allowed="getAllowed"
        @get-assigned="getAssigned"
      />
      <SideBarManageAuth :user="user" @select-auth="selectAuth" />
      {{ projectAuth }}
      <hr />
      {{ menuAuth }}
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
