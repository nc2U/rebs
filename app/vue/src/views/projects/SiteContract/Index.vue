<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <a href="/rebs/project/site-contract/" target="_blank">
        구) 사업부지 - 매매계약 관리 페이지 바로가기
      </a>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin3'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'SiteContract',
  components: {
    ContentHeader,
    ContentBody,
  },
  mixins: [HeaderMixin],
  computed: {
    ...mapState('project', ['project']),
  },
})
</script>
