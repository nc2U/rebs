<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import { type Profile } from '@/store/types/accounts'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PasswordCheck from '@/views/_MyPage/Modify/components/PasswordCheck.vue'
import ProfileForm from '@/views/_MyPage/Modify/components/ProfileForm.vue'

const accStore = useAccount()
const userInfo = computed(() => accStore.userInfo)
const profile = computed(() => accStore.profile)
const passChecked = computed(() => accStore.passChecked)

const checkPassword = (payload: { email: string; password: string }) =>
  accStore.checkPassword(payload)
const createProfile = (payload: FormData) => accStore.createProfile(payload)
const patchProfile = (payload: { pk: number; form: FormData }) => accStore.patchProfile(payload)

const checkPass = (password: string) => {
  const email = userInfo.value?.email ?? ''
  checkPassword({ email, password })
}

const onSubmit = () => 1
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <PasswordCheck v-if="!passChecked" @check-password="checkPass" />
    <ProfileForm v-else ref="profile" :profile="profile as Profile" @on-submit="onSubmit" />

    <template #footer>
      <small v-if="passChecked" />
    </template>
  </ContentBody>
</template>
