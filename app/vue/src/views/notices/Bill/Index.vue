<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useProject } from '@/store/pinia/project'
import { dateFormat } from '@/utils/baseMixins'
import { pageTitle, navMenu } from '@/views/notices/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import SalesBillIssueForm from '@/views/notices/Bill/components/SalesBillIssueForm.vue'
import ListController from '@/views/notices/Bill/components/ListController.vue'
import DownloadButton from '@/views/notices/Bill/components/DownloadButton.vue'
import ContractList from '@/views/notices/Bill/components/ContractList.vue'
import { mapActions, useStore } from 'vuex'

export default defineComponent({
  name: 'Bill',
  components: {
    ContentHeader,
    ContentBody,
    SalesBillIssueForm,
    ListController,
    DownloadButton,
    ContractList,
  },
  setup() {
    const ctor_ids = ref([])
    const billIssue = ref(null)
    const print_data = ref({
      is_bill_issue: false,
      project: null,
      pub_date: dateFormat(new Date()),
    })

    const projectStore = useProject()
    const project = computed(() => projectStore.project)
    const initProjId = computed(() => projectStore.initProjId)

    const store = useStore()
    const payOrder = computed(() => store.state.payment.payOrder)

    const payOrderTime = computed(() =>
      payOrder.value ? payOrder.value.pay_time : null,
    )
    const payOrderName = computed(() =>
      payOrder.value ? payOrder.value.__str__ : '',
    )

    return {
      pageTitle,
      navMenu,
      ctor_ids,
      billIssue,
      print_data,
      project,
      initProjId,
      payOrder,
      payOrderTime,
      payOrderName,
    }
  },

  watch: {
    project(val) {
      if (val) {
        this.billIssue = val.salesbillissue
        this.print_data.is_bill_issue = !!val.salesbillissue
        this.print_data.project = val.pk
        this.fetchPayOrder(val.salesbillissue.now_payment_order)
      }
    },
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
    this.fetchSalePriceList({ project: this.initProjId })
    this.fetchDownPayList({ project: this.initProjId })
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchPayOrderList(target)
        this.fetchOrderGroupList(target)
        this.fetchTypeList(target)
        this.fetchBuildingList(target)
        this.fetchContractList({
          project: target,
          ordering: 'contractor__name',
        })
        this.fetchSalePriceList({ project: target })
        this.fetchDownPayList({ project: target })
      } else {
        this.$store.state.payment.payOrderList = []
        this.$store.state.contract.orderGroupList = []
        this.$store.state.project.unitTypeList = []
        this.$store.state.project.buildingList = []
        this.$store.state.contract.contractList = []
        this.$store.state.contract.contractsCount = 0
        this.$store.state.contract.salesPriceList = []
        this.$store.state.contract.downPayList = []
      }
    },
    pageSelect(this: any, page: number) {
      this.ctor_ids = []
      this.$refs.listControl.listFiltering(page)
      this.$refs.contractList.unChk()
    },
    listFiltering(payload: any) {
      this.ctor_ids = []
      const project = this.project.pk
      this.fetchContractList({ ...{ project }, ...payload })
      this.$refs.contractList.unChk()
    },
    onCtorChk(payload: { chk: boolean; pk: number }) {
      let ctors: number[] = this.ctor_ids
      if (payload.chk) {
        if (!ctors.includes(payload.pk)) ctors.push(payload.pk)
      } else {
        let i = ctors.indexOf(payload.pk)
        ctors.splice(i, 1)
      }
    },
    allUnChecked() {
      this.ctor_ids = []
    },
    getNowOrder(orderPk: string) {
      this.fetchPayOrder(orderPk)
    },
    setPubDate(payload: any) {
      this.print_data.pub_date = payload
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
    ...mapActions('contract', [
      'fetchOrderGroupList',
      'fetchContractList',
      'fetchSalePriceList',
      'fetchDownPayList',
    ]),
    ...mapActions('payment', [
      'patchPayOrder',
      'fetchPayOrder',
      'fetchPayOrderList',
    ]),
    ...mapActions('project', ['fetchTypeList', 'fetchBuildingList']),
    ...mapActions('notice', ['createSalesBillIssue', 'patchSalesBillIssue']),
  },
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <SalesBillIssueForm
        :bill-issue="billIssue"
        @get-now-order="getNowOrder"
        @set-pub-date="setPubDate"
        @on-submit="onSubmit"
      />
      <ListController
        ref="listControl"
        :now_order="payOrderName"
        @list-filtering="listFiltering"
      />
      <DownloadButton :print_data="print_data" :contractors="ctor_ids" />
      <ContractList
        ref="contractList"
        :project="project"
        :now_order="payOrderTime"
        @on-ctor-chk="onCtorChk"
        @page-select="pageSelect"
        @all-un-checked="allUnChecked"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
