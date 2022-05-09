<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody>
    <ProfileForm :userInfo="userInfo" @on-submit="onSubmit" />
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
  computed: {
    ...mapState('settings', ['company']),
    ...mapState('accounts', ['userInfo']),
  },
  methods: {
    onSubmit(payload: any) {
      const { pk, ...formData } = payload
      const form = new FormData()
      for (const key in formData) {
        form.append(`${key}`, formData[key])
      }

      if (pk) this.patchProfile({ ...{ pk }, ...{ form } })
      else this.createProfile({ ...{ form } })
    },
    ...mapActions('accounts', ['createProfile', 'patchProfile']),
  },
})
</script>
