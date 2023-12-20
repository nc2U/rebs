<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import { type Profile } from '@/store/types/accounts'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PasswordCheck from '@/views/_MyPage/Modify/components/PasswordCheck.vue'
import ProfileForm from '@/views/_MyPage/Modify/components/ProfileForm.vue'

const passCheck = ref(false)
const accStore = useAccount()
const userInfo = computed(() => accStore.userInfo)
const profile = computed(() => accStore.profile)

const passwordCheck = (payload: any) => accStore.passwordCheck(payload)
const createProfile = (payload: FormData) => accStore.createProfile(payload)
const patchProfile = (payload: { pk: number; form: FormData }) => accStore.patchProfile(payload)

const onSubmit = (password: string) => {
  const email = userInfo.value?.email
  console.log({ email, password })
  // passwordCheck({ email, password })
}

const formVisible = computed(() => (passCheck.value ? 'none' : 'block'))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <PasswordCheck v-if="!passCheck" @on-submit="onSubmit" />
    <ProfileForm v-else ref="profile" :profile="profile as Profile" @on-submit="onSubmit" />

    <template #footer>
      <small v-if="passCheck" />
    </template>
  </ContentBody>
</template>
