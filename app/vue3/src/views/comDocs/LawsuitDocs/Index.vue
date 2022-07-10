<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="onSelectAdd"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <a href="/rebs/docs/lawsuit/" target="_blank">
        구) 소송 문서 관리 페이지 바로가기
      </a>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/comDocs/_menu/headermixin'
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
