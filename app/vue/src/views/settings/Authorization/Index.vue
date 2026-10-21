<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { navMenu, pageTitle } from '@/views/settings/_menu/headermixin'
import type { User } from '@/store/types/accounts'
import { useAccount, type UserByAdmin } from '@/store/pinia/account'
import Loading from '@/components/Loading/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import SettingsAuthGuard from '@/components/AuthGuard/SettingsAuthGuard.vue'
import UserSelect from './components/UserSelect.vue'
import SideBarManageAuth from './components/SideBarManageAuth.vue'
import AddUserFormModal from './components/AddUserFormModal.vue'

const refFormModal = ref()

const accStore = useAccount()
const user = computed<User | null>(() => accStore.user)

const adminCreateUser = (payload: UserByAdmin) => accStore.adminCreateUser(payload)

const selectUser = (pk: number | null) => {
  if (!!pk) {
    accStore.fetchUser(pk)
  } else {
    accStore.removeUser()
  }
}

const onSubmit = async (payload: UserByAdmin) => {
  const created = await adminCreateUser(payload)
  if (created?.pk) {
    selectUser(created.pk)
  }
}

const loading = ref(true)
onBeforeMount(async () => {
  await accStore.fetchUsersList()
  if (accStore?.userInfo) selectUser((accStore.userInfo as User).pk as number)
  loading.value = false
})
</script>

<template>
  <SettingsAuthGuard>
    <Loading v-model:active="loading" />
    <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" selector="CompanySelect" />
    <ContentBody>
      <CCardBody class="p-3 p-md-4 pb-5">
        <UserSelect
          :sel-user="user?.pk"
          @select-user="selectUser"
          @add-user-modal="refFormModal?.callModal()"
        />

        <SideBarManageAuth :user="user as User" />
      </CCardBody>

      <AddUserFormModal ref="refFormModal" @on-submit="onSubmit" />
    </ContentBody>
  </SettingsAuthGuard>
</template>
