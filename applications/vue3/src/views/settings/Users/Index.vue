<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody> Contents Here ...</ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/settings/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'UsersIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
  },
  computed: {
    ...mapState('company', ['company']),
  },
})
</script>
