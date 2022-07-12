<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <SalesBillIssueForm
        :salesbillissue="salesbillissue"
        @display-order="displayOrder"
      />
      <ListController
        ref="listControl"
        :now_order="now_order"
        @list-filtering="onListFiltering"
      />
      <DownloadButton :disabled="!isChecked" />
      {{ ctorPks }}
      <ContractList
        :project="project"
        @on-ctor-chk="onCtorChk"
        @page-select="pageSelect"
        @all-un-checked="allUnChecked"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/notices/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import SalesBillIssueForm from '@/views/notices/Bill/components/SalesBillIssueForm.vue'
import ListController from '@/views/notices/Bill/components/ListController.vue'
import DownloadButton from '@/views/notices/Bill/components/DownloadButton.vue'
import ContractList from '@/views/notices/Bill/components/ContractList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'Bill',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    SalesBillIssueForm,
    ListController,
    DownloadButton,
    ContractList,
  },
  data() {
    return {
      ctorPks: [],
      salesbillissue: null,
      now_order: '',
    }
  },
  created(this: any) {
    this.fetchPayOrderList(this.initProjId)
    this.fetchOrderGroupList(this.initProjId)
    this.fetchTypeList(this.initProjId)
    this.fetchBuildingList(this.initProjId)
    this.fetchContractList({
      project: this.initProjId,
      ordering: 'contractor__name',
    })
  },
  computed: {
    isChecked() {
      return !!this.ctorPks.length
    },
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  watch: {
    project(val) {
      this.salesbillissue = val.salesbillissue
    },
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchOrderGroupList(target)
        this.fetchTypeList(target)
        this.fetchBuildingList(target)
        this.fetchContractList({ project: target })
      } else {
        this.$store.state.contract.orderGroupList = []
        this.$store.state.project.unitTypeList = []
        this.$store.state.project.buildingList = []
        this.$store.state.contract.contractList = []
        this.$store.state.contract.contractsCount = 0
      }
    },
    pageSelect(this: any, page: number) {
      this.ctorPks = []
      this.$refs.listControl.listFiltering(page)
    },
    onListFiltering(payload: any) {
      const project = this.project.pk
      console.log(payload)
      this.fetchContractList({ ...{ project }, ...payload })
    },
    onCtorChk(payload: { chk: boolean; pk: number }) {
      let ctors: number[] = this.ctorPks
      if (payload.chk) {
        if (!ctors.includes(payload.pk)) ctors.push(payload.pk)
      } else {
        let i = ctors.indexOf(payload.pk)
        ctors.splice(i, 1)
      }
    },
    allUnChecked() {
      this.ctorPks = []
    },
    displayOrder(now_order: string) {
      this.now_order = now_order
    },
    ...mapActions('notice', ['createSalesBillIssue', 'patchSalesBillIssue']),
    ...mapActions('contract', ['fetchOrderGroupList', 'fetchContractList']),
    ...mapActions('project', ['fetchTypeList', 'fetchBuildingList']),
    ...mapActions('payment', ['fetchPayOrderList']),
  },
})
</script>
