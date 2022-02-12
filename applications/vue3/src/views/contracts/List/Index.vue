<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu">
    <IndexSummary :project="project" />
  </ContentHeader>

  <ContentBody></ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin1'
import IndexSummary from './components/IndexSummary.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ContractIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    IndexSummary,
    ContentBody,
  },
  computed: {
    ...mapState('project', ['project']),
  },
})
</script>
