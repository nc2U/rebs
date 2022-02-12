<template>
  <ContentHeader
    :page-title="'현장 문서관리'"
    :nav-menu="['현장 일반문서']"
    :selector="'ProjectSelect'"
  />
  <ContentBody> Contents Here ...</ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectGeneralDocs',
  components: {
    ContentHeader,
    ContentBody,
  },
  computed: {
    ...mapState('project', ['project']),
  },
})
</script>
