<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  >
    <ContractSummary :project="project" />
  </ContentHeader>

  <ContentBody>
    <CCardBody class="pb-5">
      <ContractList />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/contracts/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractSummary from './components/ContractSummary.vue'
import ContractList from '@/views/contracts/List/components/ContractList.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ContractIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContractSummary,
    ContractList,
  },
  computed: {
    ...mapState('project', ['project']),
  },
})
</script>
