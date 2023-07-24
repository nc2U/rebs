<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { Profile } from '@/store/types/accounts'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ProfileForm from '@/views/settings/Profile/components/ProfileForm.vue'

const image = ref<File | string | null>(null)
const accStore = useAccount()
const profile = computed(() => accStore.profile)

const fileUpload = (img: File) => (image.value = img)

const createProfile = (payload: FormData) => accStore.createProfile(payload)
const patchProfile = (payload: { pk: number; form: FormData }) =>
  accStore.patchProfile(payload)

const onSubmit = (payload: Profile & { image: File | string | null }) => {
  if (image.value) payload.image = image.value
  const { pk, ...formData } = payload
  if (!formData.user && accStore.userInfo) formData.user = accStore.userInfo.pk
  if (!formData.birth_date) formData.birth_date = ''

  const form = new FormData()

  for (const key in formData) {
    form.append(key, formData[key] as string | Blob)
  }

  if (pk) patchProfile({ ...{ pk }, ...{ form } })
  else createProfile(form)
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="CompanySelect"
  />

  <ContentBody>
    <ProfileForm
      ref="profile"
      :profile="profile as Profile"
      @file-upload="fileUpload"
      @on-submit="onSubmit"
    />
  </ContentBody>
</template>
