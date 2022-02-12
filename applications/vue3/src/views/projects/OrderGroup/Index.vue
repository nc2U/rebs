<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5" v-if="project">
      <OrderAddForm :selected="selected" @on-submit="onSubmit" />
      <OrderFormList
        @on-update="onUpdateOrder"
        @on-delete="onDeleteOrder"
        :selected="selected"
        :project="project"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ProjectMixin from '@/views/projects/projectMixin'
import OrderAddForm from '@/views/projects/OrderGroup/components/OrderAddForm.vue'
import OrderFormList from '@/views/projects/OrderGroup/components/OrderFormList.vue'
import { mapActions, mapState } from 'vuex'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import projectMixin from '@/views/projects/projectMixin'

export default defineComponent({
  name: 'ProjectsOrderSet',
  mixins: [HeaderMixin, projectMixin],
  components: {
    ContentHeader,
    ContentBody,
    OrderAddForm,
    OrderFormList,
  },
  data() {
    return {
      selected: true,
    }
  },
  created() {
    this.fetchOrderGroupList(this.initProjId)
  },
  computed: {
    ...mapState('project', ['project']),
  },
  methods: {
    projSelect(event: any) {
      if (event.target.value !== '') {
        this.selected = true
        this.fetchProject(event.target.value)
        this.fetchOrderGroupList(event.target.value)
      } else {
        this.selected = false
      }
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
