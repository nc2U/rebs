<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddProCash @multi-submit="multiSubmit" />
      <ProCashList
        :project="project"
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/proCash/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/proCash/Manage/components/ListController.vue'
import AddProCash from '@/views/proCash/Manage/components/AddProCash.vue'
import ProCashList from '@/views/proCash/Manage/components/ProCashList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectCashImprest',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ListController,
    AddProCash,
    ProCashList,
  },
  data() {
    return {
      dataFilter: {
        page: 1,
        from_date: '',
        to_date: '',
        sort: '',
        pro_acc_d1: '',
        pro_acc_d2: '',
        bank_account: '',
        search: '',
      },
    }
  },
  created() {
    this.fetchAccSortList()
    this.fetchProAllAccD1List()
    this.fetchProAllAccD2List()
    this.fetchProFormAccD1List()
    this.fetchProFormAccD2List()
    this.fetchProBankAccList(this.initProjId)
    this.fetchProjectCashList({ project: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchProBankAccList(target)
        this.fetchProjectCashList({ project: target })
      } else {
        this.$store.state.payment.proBankAccountList = []
        this.$store.state.payment.proCashBookList = []
        this.$store.state.payment.proCashesCount = 0
      }
    },
    pageSelect(this: any, page: number) {
      this.dataFilter.page = page
      this.$refs.listControl.listFiltering(page)
    },
    listFiltering(payload: any) {
      this.dataFilter = payload
      const project = this.project.pk
      const sort = payload.sort ? payload.sort : ''
      const d1 = payload.pro_acc_d1 ? payload.pro_acc_d1 : ''
      this.fetchProFormAccD1List(sort)
      this.fetchProFormAccD2List({ d1, sort })
      this.fetchProjectCashList({ ...{ project }, ...payload })
    },
    onCreate(payload: any) {
      payload.project = this.project.pk
      if (payload.sort === '3' && payload.bank_account_to) {
        const { bank_account_to, income, ...outData } = payload
        this.createPrCashBook(outData)
        const { bank_account, outlay, ...incData } = outData
        this.createPrCashBook({
          ...{ bank_account: bank_account_to, income },
          ...incData,
        })
      } else this.createPrCashBook(payload)
    },
    onUpdate(payload: any) {
      this.updatePrCashBook({ ...{ filters: this.dataFilter }, ...payload })
    },
    multiSubmit(payload: any) {
      const { formData, sepData } = payload
      console.log(formData, sepData)
      if (formData.sort) {
        if (formData.pk) this.onUpdate(formData)
        else this.onCreate(formData)
      }
      if (sepData.sort) {
        if (sepData.pk) this.onUpdate(sepData)
        else this.onCreate({ ...{ filters: this.dataFilter }, ...sepData })
      }
    },
    onDelete(payload: any) {
      this.deletePrCashBook({ ...{ filters: this.dataFilter }, ...payload })
    },
    ...mapActions('proCash', [
      'fetchAccSortList',
      'fetchProAllAccD1List',
      'fetchProAllAccD2List',
      'fetchProFormAccD1List',
      'fetchProFormAccD2List',
      'fetchProBankAccList',
      'fetchProjectCashList',
      'createPrCashBook',
      'updatePrCashBook',
      'deletePrCashBook',
    ]),
  },
})
</script>
