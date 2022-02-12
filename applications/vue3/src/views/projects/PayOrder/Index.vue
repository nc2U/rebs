<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <PayOrderAddForm :disabled="!project" @on-submit="onSubmit" />
      <PayOrderFormList
        @on-update="onUpdatePayOrder"
        @on-delete="onDeletePayOrder"
        :project="project"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PayOrderAddForm from '@/views/projects/PayOrder/components/PayOrderAddForm.vue'
import PayOrderFormList from '@/views/projects/PayOrder/components/PayOrderFormList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectsPayOrderSet',
  mixins: [HeaderMixin],
  components: {
    ContentHeader,
    ContentBody,
    PayOrderAddForm,
    PayOrderFormList,
  },
  created() {
    this.fetchPayOrderList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') this.fetchPayOrderList(target)
      else this.$store.state.cash.payOrderList = []
    },
    onSubmit(payload: any) {
      const project = this.project.pk
      this.createPayOrder({ ...{ project }, ...payload })
    },
    onUpdatePayOrder(payload: any) {
      const project = this.project.pk
      this.updatePayOrder({ ...{ project }, ...payload })
    },
    onDeletePayOrder(pk: number) {
      const project = this.project.pk
      this.deletePayOrder({ ...{ pk }, ...{ project } })
    },
    ...mapActions('cash', [
      'fetchPayOrderList',
      'createPayOrder',
      'updatePayOrder',
      'deletePayOrder',
    ]),
  },
})
</script>
