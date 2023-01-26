<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { useAccount } from '@/store/pinia/account'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UserSelect from './components/UserSelect.vue'
import ProjectManageAuth from './components/ProjectManageAuth.vue'
import SideBarManageAuth from './components/SideBarManageAuth.vue'

const comInfo = ref<{ company: number | null; is_staff: boolean }>({
  company: null,
  is_staff: true,
})

const projectAuth = ref({
  assigned_project: null as number | null,
  allowed_projects: [] as number[],
})

type Auth = '0' | '1' | '2'
export type UserAuth = {
  pk?: number
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
const menuAuth = ref<UserAuth>({
  pk: undefined,
  contract: '0',
  payment: '0',
  notice: '0',
  project_cash: '0',
  project_docs: '0',
  project: '0',
  company_cash: '0',
  company_docs: '0',
  human_resource: '0',
  company_settings: '0',
  auth_manage: '0',
})

const formsCheck = computed(() => {
  if (userInfo.value && isStaffAuth) {
    const pa = projectAuth.value
    const ma = menuAuth.value
    const sa = userInfo.value.staffauth

    const a = pa.assigned_project === sa?.assigned_project
    const b =
      JSON.stringify(pa.allowed_projects) ===
      JSON.stringify(sa?.allowed_projects)

    const c = ma.contract === sa?.contract
    const d = ma.payment === sa?.payment
    const e = ma.notice === sa?.notice
    const f = ma.project_cash === sa?.project_cash
    const g = ma.project_docs === sa?.project_docs
    const h = ma.project === sa?.project
    const i = ma.company_cash === sa?.company_cash
    const j = ma.company_docs === sa?.company_docs
    const k = ma.human_resource === sa?.human_resource
    const l = ma.company_settings === sa?.company_settings
    const m = ma.auth_manage === sa?.auth_manage
    const n = accountStore.user === null

    return (a && b && c && d && e && f && g && h && i && j && k && l && m) || n
  } else return false
})

const companyStore = useCompany()
const comId = computed(() => companyStore.company?.pk || null)

const accountStore = useAccount()
const user = computed(() => accountStore.user)
const userInfo = computed(() => accountStore.userInfo)
const isStaffAuth = computed(() => !!userInfo.value?.staffauth)

const selectUser = (pk: number | null) => {
  if (pk === null) accountStore.user = null
  else accountStore.fetchUser(pk)
}

const getAllowed = (payload: number[]) =>
  (projectAuth.value.allowed_projects = payload)
const getAssigned = (payload: number | null) =>
  (projectAuth.value.assigned_project = payload)
const selectAuth = (payload: UserAuth) => (menuAuth.value = payload)

const formSubmit = () => {
  const authData = { ...comInfo.value, ...projectAuth.value, ...menuAuth.value }
  console.log(authData)
  // accountStore.patchAuth(authData, user.value?.pk)
}

onBeforeMount(() => {
  accountStore.fetchUsersList()
  if (userInfo.value) selectUser(userInfo.value.pk as number)
  if (companyStore.company) comInfo.value.company = companyStore.company.pk
})

watch(
  () => comId.value,
  nVal => {
    if (!!nVal) comInfo.value.company = nVal
    else {
      comInfo.value.company = null
      accountStore.user = null
    }
  },
)

watch(
  () => user.value,
  nVal => {
    const sa = nVal?.staffauth
    if (nVal && sa) {
      projectAuth.value.assigned_project = sa.assigned_project
      projectAuth.value.allowed_projects = sa.allowed_projects
      menuAuth.value.pk = sa.pk
      menuAuth.value.contract = sa.contract
      menuAuth.value.payment = sa.payment
      menuAuth.value.notice = sa.notice
      menuAuth.value.project_cash = sa.project_cash
      menuAuth.value.project_docs = sa.project_docs
      menuAuth.value.project = sa.project
      menuAuth.value.company_cash = sa.company_cash
      menuAuth.value.company_docs = sa.company_docs
      menuAuth.value.human_resource = sa.human_resource
      menuAuth.value.company_settings = sa.company_settings
      menuAuth.value.auth_manage = sa.auth_manage
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
    </CCardBody>

    <CCardFooter class="text-right">
      <CButton
        type="button"
        :color="isStaffAuth ? 'success' : 'primary'"
        :disabled="formsCheck"
        @click="formSubmit"
      >
        <CIcon name="cil-check-circle" />
        저장
      </CButton>
    </CCardFooter>
  </ContentBody>
</template>
