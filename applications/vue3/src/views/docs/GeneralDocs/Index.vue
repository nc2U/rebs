<template>
  <ContentHeader
    :page-title="'본사 문서관리'"
    :nav-menu="['본사 일반문서']"
    :selector="'CompanySelect'"
  />
  <ContentBody></ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'GeneralDocs',
  components: {
    ContentHeader,
    ContentBody,
  },
  computed: {
    ...mapState('settings', ['company']),
  },
})
</script>
