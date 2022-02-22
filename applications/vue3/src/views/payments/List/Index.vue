<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  >
    <PaymentSummary :project="project" />
  </ContentHeader>

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="contControl" @cont-filtering="onContFiltering" />
      <PaymentList :project="project" @page-select="pageSelect" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/payments/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PaymentSummary from '@/views/payments/List/components/PaymentSummary.vue'
import ListController from '@/views/payments/List/components/ListController.vue'
import PaymentList from '@/views/payments/List/components/PaymentList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'PaymentsList',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    PaymentSummary,
    ListController,
    PaymentList,
  },
  created() {
    this.fetchPaymentList({ project: this.initProjId })
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') {
        this.fetchPaymentList(target)
      } else {
        this.$store.state.cash.paymentList = []
      }
    },
    pageSelect(page: number) {
      const project = this.project.pk
      this.fetchPaymentList({ ...{ project }, ...{ page } })
    },
    ...mapActions('cash', ['fetchPaymentList']),
  },
})
</script>
