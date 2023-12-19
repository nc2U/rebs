<script lang="ts" setup>
import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import { type Profile } from '@/store/types/accounts'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ProfileForm from '@/views/settings/Profile/components/ProfileForm.vue'

const accStore = useAccount()
const profile = computed(() => accStore.profile)
const isStaff = computed(
  () => useAccount().superAuth || Number(useAccount().staffAuth?.is_staff || null),
)
const profileNav = isStaff.value ? navMenu : ['프로필 관리']

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
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="profileNav" selector="CompanySelect" />

  <ContentBody>
    <ProfileForm ref="profile" :profile="profile as Profile" @on-submit="onSubmit" />

    <template #footer>
      <div style="display: none"></div>
    </template>
  </ContentBody>
</template>
