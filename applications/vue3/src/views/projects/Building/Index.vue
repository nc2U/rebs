<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody></ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'BuildingIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
  },
  computed: {
    ...mapState('project', ['project']),
  },
})
</script>
