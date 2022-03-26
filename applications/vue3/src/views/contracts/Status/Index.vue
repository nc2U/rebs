<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContSummary />
      <ExcelExport />
      <ContractBoard />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContSummary from '@/views/contracts/Status/components/ContSummary.vue'
import ExcelExport from '@/views/contracts/Status/components/ExcelExport.vue'
import ContractBoard from '@/views/contracts/Status/components/ContractBoard.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ContractStatus',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContSummary,
    ExcelExport,
    ContractBoard,
  },
  computed: {
    ...mapState('project', ['project']),
  },
})
</script>
