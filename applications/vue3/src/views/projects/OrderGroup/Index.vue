<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <ProjectSelect :project="project" @proj-select="projSelect" />
    </CCardBody>
  </CCard>

  <CCard class="mb-4 pb-5">
    <CCardHeader>
      <CIcon name="cil-notes" />
      <strong class="pl-1"> {{ $route.name }}</strong>
    </CCardHeader>

    <CCardBody v-if="project">
      <OrderAddForm :selected="selected" @on-submit="onSubmit" />
      <OrderFormList
        @on-update="onUpdateOrder"
        @on-delete="onDeleteOrder"
        :selected="selected"
        :project="project"
      />
    </CCardBody>

    <!--    <CCardFooter>&nbsp;</CCardFooter>-->
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ProjectMixin from '@/views/projects/projectMixin'
import ProjectSelect from '@/components/ProjectSelect/Index.vue'
import OrderAddForm from '@/views/projects/OrderGroup/components/OrderAddForm.vue'
import OrderFormList from '@/views/projects/OrderGroup/components/OrderFormList.vue'
import { mapActions } from 'vuex'

export default defineComponent({
  name: 'ProjectsOrderSet',
  mixins: [HeaderMixin, ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    OrderAddForm,
    OrderFormList,
  },
  created() {
    this.fetchOrderGroupList(this.initProjId)
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
