<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="onSelectAdd"
  />
  <ContentBody></ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/docs/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'lawsuitDocs',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
  },
  computed: {
    ...mapState('settings', ['company']),
  },
})
</script>
