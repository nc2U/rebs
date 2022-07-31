<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody>
    <ProfileForm
      ref="profile"
      :userInfo="userInfo"
      @file-upload="fileUpload"
      @on-submit="onSubmit"
    />
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/settings/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ProfileForm from '@/views/settings/Profile/components/ProfileForm.vue'
import { mapActions, mapState } from 'vuex'

export default defineComponent({
  name: 'ProfileIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ProfileForm,
  },
  data() {
    return {
      image: null,
    }
  },
  computed: {
    ...mapState('settings', ['company']),
    ...mapState('accounts', ['userInfo']),
  },
  methods: {
    fileUpload(image: any) {
      this.image = image
    },
    async onSubmit(this: any, payload: any) {
      const { pk, ...formData } = payload
      const form = new FormData()
      if (this.image) form.append('image', this.image)
      for (const key in formData) {
        form.append(`${key}`, formData[key])
      }

      if (pk) await this.patchProfile({ ...{ pk }, ...{ form } })
      else await this.createProfile({ ...{ form } })

      this.$refs.profile.$refs.avatar.changeImage = false
      this.$refs.profile.image = this.userInfo.profile.image
    },
    ...mapActions('accounts', ['createProfile', 'patchProfile']),
  },
})
</script>
