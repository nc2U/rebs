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
      <ContractList :project="project" @page-select="pageSelect" />
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
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContractSummary,
    ContractList,
  },
  created(this: any) {
    this.fetchContractList({ project: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') this.fetchContractList({ project: target })
      else this.$store.state.contract.contractList = []
    },
    pageSelect(page: number) {
      const project = this.project.pk
      this.fetchContractList({ project, page })
    },
    ...mapActions('contract', ['fetchContractList']),
  },
})
</script>
