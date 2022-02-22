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
      <ListController ref="listControl" @cont-filtering="onContFiltering" />
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
import ListController from '@/views/contracts/List/components/ListController.vue'
import ContractList from '@/views/contracts/List/components/ContractList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ContractIndex',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ContractSummary,
    ListController,
    ContractList,
  },
  created(this: any) {
    this.fetchOrderGroupList(this.initProjId)
    this.fetchTypeList(this.initProjId)
    this.fetchBuildingList(this.initProjId)
    this.fetchContractList({ project: this.initProjId })
    this.fetchContSummaryList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchOrderGroupList(target)
        this.fetchTypeList(target)
        this.fetchBuildingList(target)
        this.fetchContractList({ project: target })
        this.fetchContSummaryList(target)
      } else {
        this.$store.state.contract.orderGroupList = []
        this.$store.state.project.unitTypeList = []
        this.$store.state.project.buildingList = []
        this.$store.state.contract.contractList = []
        this.$store.state.contract.contractsCount = 0
      }
    },
    pageSelect(this: any, page: number) {
      this.$refs.listControl.listFiltering(page)
    },
    onContFiltering(payload: any) {
      const project = this.project.pk
      this.fetchContractList({ ...{ project }, ...payload })
    },
    ...mapActions('contract', [
      'fetchOrderGroupList',
      'fetchContractList',
      'fetchContSummaryList',
    ]),
    ...mapActions('project', ['fetchTypeList', 'fetchBuildingList']),
  },
})
</script>
