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
const profile = computed(() => accStore.profile)

const createProfile = (payload: FormData) => accStore.createProfile(payload)
const patchProfile = (payload: { pk: number; form: FormData }) => accStore.patchProfile(payload)

const onSubmit = (payload: Profile) => {
  if (!payload.image) delete payload.image

  console.log(payload)

  const { pk, ...formData } = payload
  if (!formData.user && accStore.userInfo) formData.user = accStore.userInfo.pk
  if (!formData.birth_date) formData.birth_date = ''

  const form = new FormData()

  for (const key in formData) form.append(key, formData[key] as string | Blob)

  if (pk) patchProfile({ ...{ pk }, ...{ form } })
  else createProfile(form)
}

const formVisible = computed(() => (passCheck.value ? 'none' : 'block'))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <PasswordCheck v-if="!passCheck" />
    <ProfileForm v-else ref="profile" :profile="profile as Profile" @on-submit="onSubmit" />

    <template #footer>
      <small v-if="passCheck" />
    </template>
  </ContentBody>
</template>
