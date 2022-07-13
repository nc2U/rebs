<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <SalesBillIssueForm
        :bill_issue="bill_issue"
        @display-order="displayOrder"
        @on-submit="onSubmit"
      />
      <ListController
        ref="listControl"
        :now_order="now_order"
        @list-filtering="onListFiltering"
      />
      <DownloadButton :bill_issue="bill_issue" :contractors="ctor_pk_list" />
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
      ctor_pk_list: [],
      bill_issue: null,
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
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  watch: {
    project(val) {
      this.bill_issue = val.salesbillissue
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
      this.ctor_pk_list = []
      this.$refs.listControl.listFiltering(page)
    },
    onListFiltering(payload: any) {
      const project = this.project.pk
      this.fetchContractList({ ...{ project }, ...payload })
    },
    onCtorChk(payload: { chk: boolean; pk: number }) {
      let ctors: number[] = this.ctor_pk_list
      if (payload.chk) {
        if (!ctors.includes(payload.pk)) ctors.push(payload.pk)
      } else {
        let i = ctors.indexOf(payload.pk)
        ctors.splice(i, 1)
      }
    },
    allUnChecked() {
      this.ctor_pk_list = []
    },
    displayOrder(now_order: string) {
      this.now_order = now_order
    },
    onSubmit(payload: any) {
      const { pk, now_payment_order } = payload
      const { now_due_date, ...bill_data } = payload
      if (pk) {
        this.patchPayOrder({
          pk: now_payment_order,
          pay_due_date: now_due_date,
        })
        this.patchSalesBillIssue(bill_data)
      } else {
        this.patchPayOrder({
          pk: now_payment_order,
          pay_due_date: now_due_date,
        })
        this.createSalesBillIssue(bill_data)
      }
    },
    ...mapActions('notice', ['createSalesBillIssue', 'patchSalesBillIssue']),
    ...mapActions('contract', ['fetchOrderGroupList', 'fetchContractList']),
    ...mapActions('project', ['fetchTypeList', 'fetchBuildingList']),
    ...mapActions('payment', ['fetchPayOrderList', 'patchPayOrder']),
  },
})
</script>
