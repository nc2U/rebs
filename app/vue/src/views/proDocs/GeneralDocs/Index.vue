<template>
  <ContentHeader
    :page-title="'현장 문서관리'"
    :nav-menu="['현장 일반문서']"
    :selector="'ProjectSelect'"
    @header-select="onSelectAdd"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <a href="/rebs/docs/project/general/" target="_blank">
        구) 현장 일반 문서 관리 페이지 바로가기
      </a>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
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
