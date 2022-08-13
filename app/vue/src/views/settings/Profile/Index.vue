<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { useAccount } from '@/store/pinia/accounts'
import { pageTitle, navMenu } from '@/views/settings/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ProfileForm from '@/views/settings/Profile/components/ProfileForm.vue'

const store = useStore()
const account = useAccount()

const image = ref(null)

const profile = ref()
const avatar = ref()

const company = computed(() => store.state.settings.company)
const userInfo = computed(() => account.userInfo)

const fileUpload = (image: any) => {
  image.value = image
}

const createProfile = (payload: { form: FormData }) =>
  store.dispatch('accounts/createProfile', payload)
const patchProfile = (payload: { pk: string; form: FormData }) =>
  store.dispatch('accounts/patchProfile', payload)

const onSubmit = async (payload: any) => {
  const { pk, ...formData } = payload
  const form = new FormData()
  if (image.value) form.append('image', image.value)
  for (const key in formData) {
    form.append(`${key}`, formData[key])
  }

  if (pk) await patchProfile({ ...{ pk }, ...{ form } })
  else await createProfile({ ...{ form } })

  profile.value.avatar.value.changeImage = false
  profile.value.image = userInfo.value?.profile?.image
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody>
    <ProfileForm
      ref="profile"
      :user-info="userInfo"
      @file-upload="fileUpload"
      @on-submit="onSubmit"
    />
  </ContentBody>
</template>
