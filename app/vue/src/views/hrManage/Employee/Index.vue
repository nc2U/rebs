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
import HeaderMixin from '@/views/hrManage/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Employee',
  components: {
    ContentHeader,
    ContentBody,
  },
  mixins: [HeaderMixin],
  computed: {
    ...mapState('settings', ['company']),
  },
})
</script>
