<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { type User } from '@/store/types/accounts'
import { useAccount } from '@/store/pinia/account'
import { write_auth_manage } from '@/utils/pageAuth'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import UserSelect from './components/UserSelect.vue'
import SideBarManageAuth from './components/SideBarManageAuth.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

const refAlertModal = ref()
const refConfirmModal = ref()

const comInfo = ref<{ company: number | null; is_staff: boolean }>({
  company: null,
  is_staff: false,
})

const changeStaff = (val: boolean) => {
  comInfo.value.is_staff = val
  projectAuth.value.is_project_staff = !val
}

const projectAuth = ref({
  is_project_staff: false,
  allowed_projects: [] as number[],
  assigned_project: null as number | null,
})

const changeProStaff = (val: boolean) => {
  projectAuth.value.is_project_staff = val
  comInfo.value.is_staff = !val
}

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
  if (!!user.value) {
    const pa = projectAuth.value
    const ma = menuAuth.value
    const sa = user.value.staffauth

    if (!!sa) {
      const a = comInfo.value.is_staff === sa.is_staff
      const b = pa.is_project_staff === sa.is_project_staff
      const c = JSON.stringify(pa.allowed_projects) === JSON.stringify(sa.allowed_projects)
      const d = pa.assigned_project === sa?.assigned_project
      const e = ma.contract === sa.contract
      const f = ma.payment === sa.payment
      const g = ma.notice === sa.notice
      const h = ma.project_cash === sa.project_cash
      const i = ma.project_docs === sa.project_docs
      const j = ma.project === sa.project
      const k = ma.company_cash === sa.company_cash
      const l = ma.company_docs === sa.company_docs
      const m = ma.human_resource === sa.human_resource
      const n = ma.company_settings === sa.company_settings
      const o = ma.auth_manage === sa.auth_manage

      return a && b && c && d && e && f && g && h && i && j && k && l && m && n && o
    } else {
      const a = comInfo.value.is_staff === false
      const b = pa.is_project_staff === false
      const c = JSON.stringify(pa.allowed_projects) === JSON.stringify([])
      const d = pa.assigned_project === null
      const e = ma.contract === '0'
      const f = ma.payment === '0'
      const g = ma.notice === '0'
      const h = ma.project_cash === '0'
      const i = ma.project_docs === '0'
      const j = ma.project === '0'
      const k = ma.company_cash === '0'
      const l = ma.company_docs === '0'
      const m = ma.human_resource === '0'
      const n = ma.company_settings === '0'
      const o = ma.auth_manage === '0'

      return a && b && c && d && e && f && g && h && i && j && k && l && m && n && o
    }
  } else return true
})

const comStore = useCompany()
const comId = computed(() => comStore.company?.pk)
const fetchCompany = (pk: number) => comStore.fetchCompany(pk)

const accStore = useAccount()
const user = computed(() => accStore.user)
const isStaffAuth = computed(() => !!user.value?.staffauth)

const selectUser = (pk: number | null) => {
  if (!!pk) {
    accStore.fetchUser(pk).then(() => {
      if (user.value && !user.value.staffauth) authReset()
    })
  } else {
    accStore.user = null
    authReset()
  }
}

const getAllowed = (payload: number[]) => (projectAuth.value.allowed_projects = payload)
const getAssigned = (payload: number | null) => (projectAuth.value.assigned_project = payload)
const selectAuth = (payload: UserAuth) => (menuAuth.value = payload)

const authReset = () => {
  comInfo.value.is_staff = false
  projectAuth.value.is_project_staff = false
  projectAuth.value.assigned_project = null
  projectAuth.value.allowed_projects = []
  menuAuth.value.pk = undefined
  menuAuth.value.contract = '0'
  menuAuth.value.payment = '0'
  menuAuth.value.notice = '0'
  menuAuth.value.project_cash = '0'
  menuAuth.value.project_docs = '0'
  menuAuth.value.project = '0'
  menuAuth.value.company_cash = '0'
  menuAuth.value.company_docs = '0'
  menuAuth.value.human_resource = '0'
  menuAuth.value.company_settings = '0'
  menuAuth.value.auth_manage = '0'
}

const onSubmit = () => {
  if (write_auth_manage.value) refConfirmModal.value.callModal()
  else refAlertModal.value.callModal()
}

const modalAction = () => {
  const authData = { ...comInfo.value, ...projectAuth.value, ...menuAuth.value }
  if (user.value && user.value.pk) {
    if (!!authData.pk)
      accStore.patchAuth(authData, user.value.pk) // staffauth patch
    else accStore.createAuth(authData, user.value.pk) // staffauth create
    refConfirmModal.value.close()
  } else {
    refAlertModal.value.callModal()
  }
}

watch(
  () => user.value,
  nVal => {
    const sa = nVal?.staffauth
    if (nVal && sa) {
      comInfo.value.is_staff = sa.is_staff
      projectAuth.value.is_project_staff = sa.is_project_staff
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

watch(comId, val => (!!val ? dataSetup(val) : dataReset()))

const dataSetup = (pk: number) => {
  fetchCompany(pk)
  comInfo.value.company = pk
}

const dataReset = () => {
  comInfo.value.company = null
  comStore.company = null
}

onBeforeMount(() => {
  accStore.fetchUsersList()
  comInfo.value.company = comId.value || comStore.initComId
  if (accStore?.userInfo) selectUser(accStore.userInfo.pk as number)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" selector="CompanySelect" />
  <ContentBody>
    <CCardBody>
      <UserSelect
        :sel-user="user?.pk"
        :is-staff="comInfo.is_staff"
        :is-project-staff="projectAuth.is_project_staff"
        @change-staff="changeStaff"
        @change-pro-staff="changeProStaff"
        @select-user="selectUser"
      />

      <SideBarManageAuth
        :user="user as User"
        :allowed="projectAuth.allowed_projects"
        @get-allowed="getAllowed"
        @get-assigned="getAssigned"
        @select-auth="selectAuth"
      />
    </CCardBody>

    <template #footer>
      <CCardFooter class="text-right">
        <CButton
          type="button"
          :color="isStaffAuth ? 'success' : 'primary'"
          :disabled="!comId || formsCheck"
          @click="onSubmit"
        >
          <CIcon name="cil-check-circle" />
          저장
        </CButton>
      </CCardFooter>
    </template>

    <ConfirmModal ref="refConfirmModal">
      <template #header>사용자 권한설정</template>
      <template #default>사용자 권한설정 저장을 진행하시겠습니까?</template>
      <template #footer>
        <CButton :color="isStaffAuth ? 'success' : 'primary'" @click="modalAction"> 저장</CButton>
      </template>
    </ConfirmModal>

    <AlertModal ref="refAlertModal" />
  </ContentBody>
</template>
