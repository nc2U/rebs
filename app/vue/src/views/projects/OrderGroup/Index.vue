<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <OrderAddForm :disabled="!project" @on-submit="onSubmit" />
      <OrderFormList
        :project="project"
        @on-update="onUpdateOrder"
        @on-delete="onDeleteOrder"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import OrderAddForm from '@/views/projects/OrderGroup/components/OrderAddForm.vue'
import OrderFormList from '@/views/projects/OrderGroup/components/OrderFormList.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectsOrderSet',
  components: {
    ContentHeader,
    ContentBody,
    OrderAddForm,
    OrderFormList,
  },
  mixins: [HeaderMixin],
  created() {
    this.fetchOrderGroupList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') this.fetchOrderGroupList(target)
      else this.$store.state.contract.orderGroupList = []
    },
    onSubmit(payload: any) {
      const project = this.project.pk
      this.createOrderGroup({ ...{ project }, ...payload })
    },
    onUpdateOrder(payload: any) {
      const project = this.project.pk
      this.updateOrderGroup({ ...{ project }, ...payload })
    },
    onDeleteOrder(pk: number) {
      const project = this.project.pk
      this.deleteOrderGroup({ ...{ pk }, ...{ project } })
    },
    ...mapActions('contract', [
      'fetchOrderGroupList',
      'createOrderGroup',
      'updateOrderGroup',
      'deleteOrderGroup',
    ]),
  },
})
</script>
