<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddProImprest @multi-submit="multiSubmit" />
      <TableTitleRow
        title="프로젝트 전도금 내역"
        color="success"
        excel
        disabled
      />
      <ProImprestList
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
import ListController from '@/views/proCash/Imprest/components/ListController.vue'
import AddProImprest from '@/views/proCash/Imprest/components/AddProImprest.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ProImprestList from '@/views/proCash/Imprest/components/ProImprestList.vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectImprestIndex',
  components: {
    ContentHeader,
    ContentBody,
    ListController,
    AddProImprest,
    TableTitleRow,
    ProImprestList,
  },
  mixins: [HeaderMixin],
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
    this.fetchProAccSortList()
    this.fetchProAllAccD1List()
    this.fetchProAllAccD2List()
    this.fetchProFormAccD1List()
    this.fetchProFormAccD2List()
    this.fetchProBankAccList(this.initProjId)
    this.fetchProjectImprestList({ project: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchProBankAccList(target)
        this.fetchProjectImprestList({ project: target })
      } else {
        this.FETCH_P_BANK_ACCOUNT_LIST([])
        this.FETCH_P_IMPREST_LIST({ results: [], count: 0 })
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
      this.fetchProjectImprestList({ ...{ project }, ...payload })
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
      'fetchProAccSortList',
      'fetchProAllAccD1List',
      'fetchProAllAccD2List',
      'fetchProFormAccD1List',
      'fetchProFormAccD2List',
      'fetchProBankAccList',
      'fetchProjectImprestList',
      'createPrCashBook',
      'updatePrCashBook',
      'deletePrCashBook',
    ]),
    ...mapMutations('proCash', [
      'FETCH_P_BANK_ACCOUNT_LIST',
      'FETCH_P_IMPREST_LIST',
    ]),
  },
})
</script>
