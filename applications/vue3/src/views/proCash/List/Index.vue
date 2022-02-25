<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @payment-filtering="onPayFiltering" />
      <ProCashList
        :project="project"
        @page-select="pageSelect"
        @on-update="onUpdate"
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
import ListController from '@/views/proCash/List/components/ListController.vue'
import ProCashList from '@/views/proCash/List/components/ProCashList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectCashList',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    ListController,
    ProCashList,
  },
  created() {
    this.fetchProjectBankAccountList(this.initProjId)
    this.fetchProjectCashList({ project: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchProjectBankAccountList(target)
        this.fetchProjectCashList({ project: target })
      } else {
        this.$store.state.payment.proBankAccountList = []
        this.$store.state.payment.proCashBookList = []
        this.$store.state.payment.proCashesCount = 0
      }
    },
    pageSelect(this: any, page: number) {
      this.$refs.listControl.listFiltering(page)
    },
    onPayFiltering(payload: any) {
      const project = this.project.pk
      this.fetchProjectCashList({ ...{ project }, ...payload })
    },
    onUpdate(payload: any) {
      console.log(payload)
    },
    onDelete(pk: number) {
      alert(pk)
    },
    ...mapActions('proCash', [
      'fetchProjectBankAccountList',
      'fetchProjectCashList',
    ]),
  },
})
</script>
