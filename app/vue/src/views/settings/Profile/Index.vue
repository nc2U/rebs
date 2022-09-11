<script lang="ts" setup>
import { computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { Profile } from '@/store/types/accounts'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ProfileForm from '@/views/settings/Profile/components/ProfileForm.vue'

// const profile = ref()
// const image = ref(null)

const accountStore = useAccount()
const profile = computed(() => accountStore.profile)

// const fileUpload = (image: File) => (image.value = image)

const createProfile = (payload: FormData) => console.log(payload) // accountStore.createProfile(payload)
const patchProfile = (payload: { pk: number } & FormData) =>
  console.log(payload) //  accountStore.patchProfile(payload)

const onSubmit = async (payload: Profile) => {
  const { pk, ...formData } = payload
  const form = new FormData()

  for (const key in formData as any) {
    // form.append(key, formData[key])
    console.log(key, formData[key])
  }

  console.log(form)

  // if (pk) await patchProfile({ ...{ pk }, ...form })
  // else await createProfile({ ...form })

  // profile.value.avatar.value.changeImage = false
  // profile.value.image = userInfo.value?.profile?.image
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody>
    <ProfileForm ref="profile" :profile="profile" @on-submit="onSubmit" />
  </ContentBody>
</template>
