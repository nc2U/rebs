<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu"></ContentHeader>

  <ContentBody> Contents Here ...</ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projectCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectCashStatus',
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
